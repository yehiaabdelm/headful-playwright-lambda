import subprocess, os, json, base64, time
from playwright.sync_api import sync_playwright


def start_xvfb():
    """Start Xvfb with settings optimized for Lambda environment"""
    os.environ["DISPLAY"] = ":99"
    try:
        subprocess.Popen([
            "Xvfb", 
            ":99", 
            "-screen", "0", "1280x1024x24", 
            "-nolisten", "tcp", 
            "-nolisten", "unix",
            "-ac",  # Disable access control
            "-fp", "/usr/share/fonts/X11/misc"
        ])
        # Give Xvfb a moment to start up
        time.sleep(2)
    except Exception as e:
        print(f"Error starting Xvfb: {e}")


def take_screenshot(url="https://google.com", viewport=None, timeout=60000):
    """Take a screenshot of the specified URL with optional viewport dimensions"""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--single-process"  # Important for containerized environments
                ]
            )
            
            if viewport is None:
                viewport = {"width": 1280, "height": 720}
                
            page = browser.new_page(viewport=viewport)
            page.goto(url, timeout=timeout)
            page.wait_for_timeout(3000)
            
            screenshot_path = "/tmp/screenshot.png"
            page.screenshot(path=screenshot_path)
            
            browser.close()
            return screenshot_path
    except Exception as e:
        print(f"Error in take_screenshot: {e}")
        raise


def lambda_handler(event, context=None):
    """AWS Lambda handler function"""
    start_xvfb()
    
    try:
        body = {}
        if event.get('body'):
            body = json.loads(event['body'])
        
        url = body.get('url', 'https://google.com')
        
        viewport = None
        if 'width' in body and 'height' in body:
            viewport = {
                "width": int(body['width']),
                "height": int(body['height'])
            }
        
        screenshot_path = take_screenshot(url, viewport)
        
        with open(screenshot_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("utf-8")
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Screenshot taken successfully",
                "image_base64": encoded_image
            })
        }
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }