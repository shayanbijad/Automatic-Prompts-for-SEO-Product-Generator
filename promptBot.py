import time
from openai import OpenAI
import os

# تنظیمات API
client = OpenAI(
    api_key="yourkey",
    base_url="https://api.deepseek.com"
)

def get_deepseek_response(prompt):
    """دریافت پاسخ از DeepSeek با مدیریت خطاها"""
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            timeout=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"<p style='color: red;'>خطا در پردازش: {e}</p>"

def format_html(content, title=None):
    """قالب‌بندی محتوا به HTML"""
    if title:
        return f"<h2>{title}</h2>\n<div>{content}</div>"
    return f"<div>{content}</div>"

def ask_questions(product_name, titles, features, short_description):
    """پرسش‌های اصلی + پرامپت کوتاه‌نویسی با ورودی کاربر"""
    prompts = {
        "Review": f"{product_name} را به صورت تخصصی بررسی کن و مزایا و معایبش رو بنویس.",
        "Paragraphs": f"برای هر یک از این عناوین یک پاراگراف بنویس: {', '.join(titles)}",
        "Table": f"ویژگی‌های زیر را به صورت یک جدول HTML مرتب کن (با تگ‌های <table>): {', '.join(features)}",
        "Meta": f"یک متن توضیح متای ۱۵۰ کاراکتری برای محصول {product_name} بنویس.",
        "Short": f"این ها رو هم کوتاه بازنویسی میکنی مثل خودش: {short_description}"
    }
    
    responses = {}
    for key, prompt in prompts.items():
        responses[key] = get_deepseek_response(prompt)
        time.sleep(5)
    
    return responses

def save_to_html(product_name, data):
    """ذخیره خروجی به صورت HTML"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>بررسی {product_name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            h2 {{ color: #2c3e50; border-bottom: 1px solid #eee; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
        </style>
    </head>
    <body>
        <h1>بررسی محصول {product_name}</h1>
        {format_html(data['Review'], 'بررسی تخصصی')}
        {format_html(data['Paragraphs'], 'پاراگراف‌های توصیفی')}
        {format_html(data['Table'], 'جدول ویژگی‌ها')}
        {format_html(data['Short'], 'خلاصه کوتاه')}
        {format_html(data['Meta'], 'توضیح متا (SEO)')}
    </body>
    </html>
    """
    
    file_name = f"{product_name}_review.html"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"خروجی HTML در فایل {file_name} ذخیره شد.")

# اجرای اصلی
if __name__ == "__main__":
    product_name = input("product name: ")
    titles = input("titles to write a paragraph for: ").split(',')
    features = input("table features: ").split(',')
    short_description = input("short description: ")
    
    responses = ask_questions(product_name, titles, features, short_description)
    save_to_html(product_name, responses)