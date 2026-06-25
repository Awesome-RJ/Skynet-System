from Skynet_System import system_cmd, System
from PIL import Image, ImageDraw, ImageFont
import os


@System.on(system_cmd(pattern=r"get_id"))
async def image_maker(event) -> None:
    replied_user = await event.get_reply_message()
    if replied_user:
        target_user = replied_user.sender
        target_id = replied_user.sender_id
    else:
        target_user = await event.get_sender()
        target_id = event.sender_id

    if not target_user or not target_id:
        await event.reply("Could not identify target user.")
        return

    photo_path = "user.png"
    if os.path.exists(photo_path):
        try:
            os.remove(photo_path)
        except Exception:
            pass

    # Download profile photo
    await System.download_profile_photo(
        target_id, file=photo_path, download_big=True
    )

    if os.path.exists(photo_path):
        user_photo = Image.open(photo_path)
        user_photo = user_photo.resize((1159, 1241))
    else:
        # Fallback placeholder if user has no profile photo
        user_photo = Image.new('RGB', (1159, 1241), color=(180, 180, 180))

    # open id photo
    id_template = Image.open("ID.png")
    # put image in position
    id_template.paste(user_photo, (1003, 641))
    # postion on where to draw text
    draw = ImageDraw.Draw(id_template)
    color = "rgb(0, 0, 0)"  # black
    font = ImageFont.truetype("font.ttf", size=80)
    font2 = ImageFont.truetype("font2.ttf", size=100)
    # put text in image
    first_name = (target_user.first_name or "User").replace("\u2060", "")
    draw.text(
        (1000, 460),
        first_name,
        fill=color,
        font=font2,
    )
    draw.text((393, 50), str(target_id), fill=color, font=font)
    id_template.save("user_id.png")
    force_document = "doc" in event.text
    await System.send_message(
        event.chat_id,
        "Generated User ID",
        reply_to=event.message.id,
        file="user_id.png",
        force_document=force_document,
        silent=True,
    )
    
    # Cleanup files safely
    for temp_file in ["user_id.png", photo_path]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except Exception:
                pass
