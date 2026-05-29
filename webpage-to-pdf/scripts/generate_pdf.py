import sys
import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_pdf.py <URL> <OUTPUT_PATH>")
        sys.exit(1)
        
    url = sys.argv[1]
    desktop_path = sys.argv[2]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1200, 'height': 800},
            device_scale_factor=1
        )
        page = await context.new_page()
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # Scroll to bottom for lazy loading
        print("Scrolling down to load images...")
        await page.evaluate("""
            async () => {
                await new Promise((resolve) => {
                    let totalHeight = 0;
                    const distance = 300;
                    const timer = setInterval(() => {
                        const scrollHeight = document.body.scrollHeight;
                        window.scrollBy(0, distance);
                        totalHeight += distance;
                        if(totalHeight >= scrollHeight){
                            clearInterval(timer);
                            resolve();
                        }
                    }, 50);
                });
            }
        """)
        
        print("Cleaning up page layout...")
        # Hide unneeded elements
        await page.add_style_tag(content="""
            .header, .left_contents, .unit_utility, .footer, .ad_top, .hot_game_now, .right_contents, iframe, .side_menu, .V2_utility, .V2_global_navi, .recommend_article, .ContentsBottom_dynamic, .ad_bottom, .PC_JACK {
                display: none !important;
            }
            .unit_contents, .main_contents, .contents, main, article {
                width: 100% !important;
                max-width: 100% !important;
                margin: 0 !important;
                padding: 0 !important;
                float: none !important;
                background-color: white !important;
            }
            body {
                background-color: white !important;
            }
        """)
        
        # Wait for images to load
        await page.wait_for_timeout(3000)
        
        print(f"Saving PDF to {desktop_path}...")
        await page.pdf(path=desktop_path, format="A4", print_background=True, margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"})
        
        await browser.close()
        print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
