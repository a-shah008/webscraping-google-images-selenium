
# This script automatically web scrapes an x number of images in a web 
# browser based off of what type of image you want using requests and image class names.
# Several aspects of what you are looking for can be modified. For example, this script searched for supercars, 
# but with very minimal tweaking in the code, you can search for anything, such as dogs, cats, etc.

# The images that are web scraped are not actually
# downloaded to the system, instead they are just printed out.

# DISCLAIMER: This only works for Google Chrome Images (version: 94...) as of right now

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time
PATH = f"C:/Users/Atithi/Desktop/Coding/WebScraping/chromedriver.exe"

no_errors = True
while no_errors:
    try:

        wd = webdriver.Chrome(PATH)

        def get_images_from_google(wd, delay, max_images):
            def scroll_down(wd):
                wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(delay)
            
            # To change the image you want to find (PART 1), first change this URL with the URL of what you want to look:
            url = "https://www.google.com/search?q=luxury+cars&rlz=1C1CHBF_enUS749US749&sxsrf=AOaemvKU5JaXr7bln5nBQV6S_OQve_Kksg:1636161499082&source=lnms&tbm=isch&sa=X&ved=2ahUKEwibpMrHyIL0AhUCH80KHRFUA6IQ_AUoAXoECAIQAw&biw=1920&bih=969&dpr=1"
            
            
            wd.get(url)

            image_urls = set()
            skips = 0

            while len(image_urls) + skips < max_images:
                scroll_down(wd)
                thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
                for img in thumbnails[len(image_urls):max_images]:
                    try:
                        img.click()
                        time.sleep(delay)
                    except:
                        continue
                    
                    images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
                    for image in images:
                        if image.get_attribute("src") in image_urls:
                            max_images += 1
                            skips += 1

                            print("Duplicate image found, proceeding to initialize backup plan (this is okay).")
                            break

                        if image.get_attribute('src') and 'https' in image.get_attribute('src'):
                            image_urls.add(image.get_attribute('src'))
                            print(f"\nFound {len(image_urls)} out of {max_images - skips}\n")
            
            return f"\n{image_urls}\n"

        # The following function is not being used:
        def download_image(download_path, url, file_name):
            try:
                image_content = requests.get(url).content
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file)
                file_path = download_path + file_name

                with open(file_path, "wb") as f:
                    image.save(f, "JPEG")
                
                print("Success")
            except Exception as e:
                print('FAILED -', e)


        urls = get_images_from_google(wd, 1, 10)

        print(urls)
        print("\nSuccess! Script has finished running.")
        wd.quit()
        break

    except Exception:
        no_errors = False
        print("A problem in the code was detected. Automatically aborting script.")
        wd.quit()
        break
