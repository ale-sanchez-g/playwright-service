from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import asyncio
from playwright.async_api import async_playwright
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(title="Playwright Testing Service")

class TestPlan(BaseModel):
    test_plan: Dict[str, Any]
    url: str
    record_video: bool = True  # Add record_video parameter

class NavigateRequest(BaseModel):
    url: str

# Create an endpoint to ensure the service is running
@app.get("/")
async def read_root():
    return {"status": "ok"}

@app.post("/execute")
async def execute_test(test_request: TestPlan):
    """Execute a test plan on a website using Playwright."""
    # Log the test request
    print(f"Received test request for URL: {test_request.url}")
    print(f"Test plan: {json.dumps(test_request.test_plan, indent=2)}")
    
    try:
        results = await run_test(test_request.url, test_request.test_plan, test_request.record_video)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test execution failed: {str(e)}")

@app.post("/navigate")
async def navigate_to_url(request: NavigateRequest):
    """Navigate to a URL, ensure all elements load (including JavaScript), and return a map of all elements."""
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
                java_script_enabled=True
            )  # Ensure JavaScript is enabled
            page = await context.new_page()
            await page.goto(request.url)
            # if element #root is not loaded, wait for body
            if not await page.query_selector("#root"):
                await page.wait_for_selector("body")
            else:
                # Wait for the React app to load
                await page.wait_for_selector("#root") 
            
            # Extract all elements inside the React app
            elements = await page.evaluate('''() => {
                const allElements = document.querySelectorAll('*');
                return Array.from(allElements).map(el => ({
                    tag: el.tagName,
                    class: el.className,
                    id: el.id,
                    text: el.innerText
                }));
            }''')
            
            await browser.close()
            return {"url": request.url, "elements": elements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Navigation failed: {str(e)}")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.yaml", title="Playwright Testing Service")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

async def run_test(url: str, test_plan: Dict[str, Any], record_video: bool):
    """Run the actual Playwright test based on the provided test plan."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            record_video_dir="static/videos" if record_video else None  # Enable video recording if requested
        )
        
        # Create a new page
        page = await context.new_page()
        
        # Navigate to the URL
        await page.goto(url)
        
        results = {
            "steps": [],
            "success": True,
            "error": None,
            "screenshots": [],
            "video": None
        }
        
        # Process each step in the test plan
        for step_index, step in enumerate(test_plan.get("steps", [])):
            step_result = await process_step(page, step, step_index)
            results["steps"].append(step_result)
            
            # If the step failed, mark the entire test as failed
            if not step_result["success"]:
                results["success"] = False
                results["error"] = f"Step failed: {step_result['step']}"
                break
        
        # Take a final screenshot
        final_screenshot = "final_state.png"
        await page.screenshot(path=final_screenshot)
        results["screenshots"].append(final_screenshot)
        
        # Save video path if recording was enabled
        if record_video:
            video_path = await page.video.path()
            results["video"] = video_path
        
        # Close the browser
        await browser.close()
        
        return results

async def process_step(page, step, step_index):
    """Process a single step in the test plan."""
    step_result = {
        "step": step.get("description", f"Step {step_index+1}"),
        "success": False,
        "details": {}
    }
    
    try:
        action_type = step.get("action", "").lower()
        selector = step.get("selector", "")
        value = step.get("value", "")
        
        if action_type == "click":
            await page.click(selector)
            step_result["details"]["action"] = f"Clicked on {selector}"
        
        elif action_type == "hover":
            await page.hover(selector)
            step_result["details"]["action"] = f"Hovered over {selector}"

        elif action_type == "type":
            await page.fill(selector, value)
            step_result["details"]["action"] = f"Typed '{value}' into {selector}"
        
        elif action_type == "scroll":
            await page.evaluate(f'document.querySelector("{selector}").scrollIntoView()')
            step_result["details"]["action"] = f"Scrolled to {selector}"

        elif action_type == "navigate":
            await page.goto(value)
            step_result["details"]["action"] = f"Navigated to {value}"
        
        elif action_type == "wait":
            wait_time = step.get("value", 3000)  # Default to 3000 ms if not specified
            await page.wait_for_timeout(wait_time)
            step_result["details"]["action"] = f"Waited for {wait_time} ms"
        
        elif action_type == "waitforloadstate":
            load_state = step.get("state", "load")  # Default to 'load' if not specified
            await page.wait_for_load_state(load_state)
            step_result["details"]["action"] = f"Waited for load state '{load_state}'"
        
        elif action_type == "check":
            is_visible = await page.is_visible(selector)
            step_result["details"]["action"] = f"Checked visibility of {selector}"
            step_result["details"]["result"] = f"Element is {'visible' if is_visible else 'not visible'}"
            
            if step.get("expect_visible", True) != is_visible:
                step_result["success"] = False
                step_result["details"]["error"] = "Visibility check failed"
            else:
                step_result["success"] = True
        
        elif action_type == "screenshot":
            screenshot_path = f"screenshot_{step_index}.png"
            await page.screenshot(path=screenshot_path)
            step_result["details"]["action"] = "Took screenshot"
            step_result["details"]["screenshot"] = screenshot_path
        
        # Add more action types as needed
        
        else:
            step_result["details"]["error"] = f"Unknown action type: {action_type}"
            step_result["success"] = False
        
        # If we got here without an error, and it's not a check action (which sets its own success),
        # mark the step as successful
        if action_type != "check" and "error" not in step_result["details"]:
            step_result["success"] = True
        
    except Exception as e:
        step_result["success"] = False
        step_result["details"]["error"] = str(e)
    
    return step_result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)