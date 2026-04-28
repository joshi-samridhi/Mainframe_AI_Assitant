"""
Mainframe Error Screen Image Generator
Generates annotated terminal screen images for common mainframe error codes
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Color definitions
BG_COLOR = "#0a0a0a"  # Dark terminal background
TEXT_COLOR = "#00ff00"  # Green mainframe text
RED_COLOR = "#ff0000"  # Error highlights
WHITE_COLOR = "#ffffff"  # Annotations
YELLOW_COLOR = "#ffff00"  # Additional highlights

# Image dimensions
WIDTH = 1400
HEIGHT = 900

def get_font(size=16):
    """Get monospace font for terminal appearance"""
    try:
        return ImageFont.truetype("cour.ttf", size)
    except:
        try:
            return ImageFont.truetype("courier.ttf", size)
        except:
            return ImageFont.load_default()

def draw_box(draw, x, y, width, height, color, thickness=2):
    """Draw a rectangle box"""
    for i in range(thickness):
        draw.rectangle([x-i, y-i, x+width+i, y+height+i], outline=color)

def draw_circle(draw, x, y, radius, color, thickness=2):
    """Draw a circle"""
    for i in range(thickness):
        draw.ellipse([x-radius-i, y-radius-i, x+radius+i, y+radius+i], outline=color)

def draw_arrow(draw, x1, y1, x2, y2, color, thickness=2):
    """Draw an arrow from (x1,y1) to (x2,y2)"""
    draw.line([x1, y1, x2, y2], fill=color, width=thickness)
    # Arrow head
    angle = 0.5
    length = 15
    import math
    dx = x2 - x1
    dy = y2 - y1
    norm = math.sqrt(dx*dx + dy*dy)
    if norm > 0:
        dx /= norm
        dy /= norm
        # Left arrow head
        draw.line([x2, y2, x2 - length*(dx*math.cos(angle) + dy*math.sin(angle)),
                   y2 - length*(dy*math.cos(angle) - dx*math.sin(angle))], 
                  fill=color, width=thickness)
        # Right arrow head
        draw.line([x2, y2, x2 - length*(dx*math.cos(angle) - dy*math.sin(angle)),
                   y2 - length*(dy*math.cos(angle) + dx*math.sin(angle))], 
                  fill=color, width=thickness)

def generate_u0777_screen():
    """Generate U0777 - Data Validation Abend error screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(20)
    font_medium = get_font(16)
    font_small = get_font(14)
    
    # Main terminal content
    y = 40
    draw.text((40, y), "JOBNAME: DUMMYBATCH01", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "JOBID: 12345", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "STATUS: ABEND", TEXT_COLOR, font=font_medium)
    y += 30
    
    # Return code with red box
    return_code_y = y
    draw.text((40, y), "RETURN CODE: ", TEXT_COLOR, font=font_medium)
    draw.text((200, y), "U0777", TEXT_COLOR, font=font_medium)
    draw_box(draw, 195, y-5, 80, 25, RED_COLOR, 3)
    y += 30
    
    # Step with red highlight
    step_y = y
    draw.text((40, y), "STEP: ", TEXT_COLOR, font=font_medium)
    draw.rectangle([120, y-5, 220, y+20], fill=RED_COLOR)
    draw.text((125, y), "STEP002", BG_COLOR, font=font_medium)
    y += 30
    
    draw.text((40, y), "ERROR: DATA VALIDATION FAILED", TEXT_COLOR, font=font_medium)
    y += 50
    
    # Job Log section
    draw.text((40, y), "Job Log:", TEXT_COLOR, font=font_large)
    y += 35
    draw.text((40, y), "Invalid record ", TEXT_COLOR, font=font_medium)
    record_x = 220
    draw.text((record_x, y), "RECORD#007", TEXT_COLOR, font=font_medium)
    draw.text((360, y), ", STEP002 ended abnormally", TEXT_COLOR, font=font_medium)
    
    # Circle the record
    draw_circle(draw, record_x + 60, y + 10, 60, RED_COLOR, 3)
    
    # Arrow pointing to record
    draw_arrow(draw, record_x + 60, y + 80, record_x + 60, y + 40, YELLOW_COLOR, 3)
    
    y += 100
    
    # Label
    draw.text((40, y), "U0777 - Data validation abend", YELLOW_COLOR, font=font_large)
    
    # Resolution Checklist (right side)
    checklist_x = 850
    checklist_y = 100
    draw_box(draw, checklist_x - 10, checklist_y - 10, 480, 280, TEXT_COLOR, 3)
    draw.text((checklist_x, checklist_y), "Resolution Checklist", TEXT_COLOR, font=font_large)
    checklist_y += 40
    
    steps = [
        "1) Isolate RECORD#007",
        "2) Check copybook format",
        "3) Fix invalid data",
        "4) Re-run STEP002"
    ]
    
    for step in steps:
        draw.text((checklist_x + 20, checklist_y), step, TEXT_COLOR, font=font_medium)
        checklist_y += 50
    
    img.save('mainframe-error-screens/output/U0777_error_screen.png')
    print("✓ Generated U0777_error_screen.png")

def generate_s013_screen():
    """Generate S013 - Dataset Open Error screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(20)
    font_medium = get_font(16)
    font_small = get_font(14)
    
    # Main terminal content
    y = 40
    draw.text((40, y), "JOBNAME: DUMMYBATCH01", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "JOBID: 12345", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "STATUS: ABEND", TEXT_COLOR, font=font_medium)
    y += 30
    
    # Return code with red box
    draw.text((40, y), "RETURN CODE: ", TEXT_COLOR, font=font_medium)
    draw.text((200, y), "S013", TEXT_COLOR, font=font_medium)
    draw_box(draw, 195, y-5, 70, 25, RED_COLOR, 3)
    y += 30
    
    # Step with red highlight
    draw.text((40, y), "STEP: ", TEXT_COLOR, font=font_medium)
    draw.rectangle([120, y-5, 220, y+20], fill=RED_COLOR)
    draw.text((125, y), "STEP005", BG_COLOR, font=font_medium)
    y += 30
    
    draw.text((40, y), "ERROR: DATASET OPEN ERROR (DCB / RECFM MISMATCH)", TEXT_COLOR, font=font_medium)
    y += 50
    
    # Job Log section
    draw.text((40, y), "Job Log:", TEXT_COLOR, font=font_large)
    y += 35
    draw.text((40, y), "IEC141I 013-20, DUMMYBATCH01, STEP005, DDNAME ", TEXT_COLOR, font=font_medium)
    ddname_x = 600
    draw.rectangle([ddname_x-5, y-5, ddname_x+85, y+20], fill=YELLOW_COLOR)
    draw.text((ddname_x, y), "INPUT1", BG_COLOR, font=font_medium)
    y += 30
    
    error_msg_y = y
    draw.text((40, y), "Dataset attribute mismatch - ", TEXT_COLOR, font=font_medium)
    error_x = 380
    draw.text((error_x, y), "RECFM or LRECL incorrect", TEXT_COLOR, font=font_medium)
    
    # Circle the error message
    draw_circle(draw, error_x + 140, y + 10, 140, RED_COLOR, 3)
    
    # Arrow pointing to error
    draw_arrow(draw, error_x + 140, y + 160, error_x + 140, y + 60, YELLOW_COLOR, 3)
    
    y += 180
    
    # Label
    draw.text((40, y), "S013 - Dataset open error", YELLOW_COLOR, font=font_large)
    
    # Resolution Checklist (right side)
    checklist_x = 850
    checklist_y = 100
    draw_box(draw, checklist_x - 10, checklist_y - 10, 480, 280, TEXT_COLOR, 3)
    draw.text((checklist_x, checklist_y), "Resolution Checklist", TEXT_COLOR, font=font_large)
    checklist_y += 40
    
    steps = [
        "1) Check DD statement in JCL",
        "2) Verify RECFM and LRECL",
        "3) Compare with dataset attributes",
        "4) Correct JCL and re-run job"
    ]
    
    for step in steps:
        draw.text((checklist_x + 20, checklist_y), step, TEXT_COLOR, font=font_medium)
        checklist_y += 50
    
    img.save('mainframe-error-screens/output/S013_error_screen.png')
    print("✓ Generated S013_error_screen.png")

def generate_s0c7_screen():
    """Generate S0C7 - Numeric Data Exception screen"""
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    font_large = get_font(20)
    font_medium = get_font(16)
    font_small = get_font(14)
    
    # Main terminal content
    y = 40
    draw.text((40, y), "JOBNAME: DUMMYBATCH01", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "JOBID: 67890", TEXT_COLOR, font=font_medium)
    y += 30
    draw.text((40, y), "STATUS: ABEND", TEXT_COLOR, font=font_medium)
    y += 30
    
    # Return code with red box
    draw.text((40, y), "RETURN CODE: ", TEXT_COLOR, font=font_medium)
    draw.text((200, y), "S0C7", TEXT_COLOR, font=font_medium)
    draw_box(draw, 195, y-5, 70, 25, RED_COLOR, 3)
    y += 30
    
    # Step with red highlight
    draw.text((40, y), "STEP: ", TEXT_COLOR, font=font_medium)
    draw.rectangle([120, y-5, 220, y+20], fill=RED_COLOR)
    draw.text((125, y), "STEP010", BG_COLOR, font=font_medium)
    y += 30
    
    draw.text((40, y), "ERROR: DATA EXCEPTION", TEXT_COLOR, font=font_medium)
    y += 50
    
    # Job Log section
    draw.text((40, y), "Job Log:", TEXT_COLOR, font=font_large)
    y += 35
    draw.text((40, y), "Invalid numeric data in field ", TEXT_COLOR, font=font_medium)
    field_x = 400
    draw.text((field_x, y), "AMOUNT", TEXT_COLOR, font=font_medium)
    draw.text((field_x + 100, y), ", STEP010 failed", TEXT_COLOR, font=font_medium)
    
    # Circle the field
    draw_circle(draw, field_x + 45, y + 10, 60, RED_COLOR, 3)
    
    # Arrow pointing to field
    draw_arrow(draw, field_x + 45, y + 80, field_x + 45, y + 40, YELLOW_COLOR, 3)
    
    y += 100
    
    # Label
    draw.text((40, y), "S0C7 - Numeric data exception", YELLOW_COLOR, font=font_large)
    
    # Resolution Checklist (right side)
    checklist_x = 850
    checklist_y = 100
    draw_box(draw, checklist_x - 10, checklist_y - 10, 480, 280, TEXT_COLOR, 3)
    draw.text((checklist_x, checklist_y), "Resolution Checklist", TEXT_COLOR, font=font_large)
    checklist_y += 40
    
    steps = [
        "1) Check numeric fields",
        "2) Remove invalid characters",
        "3) Validate input data",
        "4) Re-run job"
    ]
    
    for step in steps:
        draw.text((checklist_x + 20, checklist_y), step, TEXT_COLOR, font=font_medium)
        checklist_y += 50
    
    img.save('mainframe-error-screens/output/S0C7_error_screen.png')
    print("✓ Generated S0C7_error_screen.png")

def main():
    """Generate all error screen images"""
    print("Mainframe Error Screen Generator")
    print("=" * 50)
    print("\nGenerating annotated error screens...\n")
    
    # Create output directory if it doesn't exist
    os.makedirs('mainframe-error-screens/output', exist_ok=True)
    
    # Generate all three error screens
    generate_u0777_screen()
    generate_s013_screen()
    generate_s0c7_screen()
    
    print("\n" + "=" * 50)
    print("✓ All error screens generated successfully!")
    print("Images saved in: mainframe-error-screens/output/")
    print("\nGenerated files:")
    print("  - U0777_error_screen.png")
    print("  - S013_error_screen.png")
    print("  - S0C7_error_screen.png")

if __name__ == "__main__":
    main()

# Made with Bob
