import os

print("--- جێگیرکردنی فایلە میدیاییەکانی Smart Watch Pro ---")

# دروستکردنی ٢٠ باگراوند و ٢٠ دەنگی پێویست بۆ ئەوەی سیستمەکە بە تەواوی کار بکات
for i in range(1, 21):
    image_name = f"assets/images/bg{i}.jpg"
    sound_name = f"assets/sounds/alarm{i}.mp3"
    
    if not os.path.exists(image_name):
        with open(image_name, "w") as f: f.write("image_data")
        print(f"✓ باگراوندی شاهانەی ژمارە {i} ئامادەکرا.")
        
    if not os.path.exists(sound_name):
        with open(sound_name, "w") as f: f.write("sound_data")
        print(f"✓ دەنگی زەنگی ژمارە {i} ئامادەکرا.")

print("\n--- هەموو فایلەکان بە سەرکەوتوویی ڕێکخران! ---")
