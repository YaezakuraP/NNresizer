from PIL import Image
import glob
import os
from concurrent import futures

FileTypes = ['/*.jpg','/*.png','/*.JPG','/*.PNG']

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

#--------------------------------------------------

# 並列化用関数
def task_crop(target_file):
    img = Image.open(target_file)
    filename = os.path.basename(target_file)

    # ----正方形にする---
    img = crop_center(img,min(img.size),min(img.size))
    img = img.resize((resized_size,resized_size))

    print('Processing: ',target_file)

    # ファイルを保存
    img.save(f'{output_dir}/{filename}')


input_dir = input('Input data path:').replace('\\','/').replace('"','').replace("'",'')
output_dir = input_dir+'/resized'
resized_size = int(input('Input resized size:'))

# 出力先フォルダの作成
os.makedirs(output_dir,exist_ok=True)


# フォルダの中身を確認
for FileType in FileTypes:
    files = glob.glob(input_dir+FileType)
    # クロップ作業
    with futures.ThreadPoolExecutor() as executor:
        for i,file in enumerate(files):
            executor.submit(task_crop,file)
