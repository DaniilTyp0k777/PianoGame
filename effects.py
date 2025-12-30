from typing import Optional

from pygame import draw, transform, image
from settings import BLACK


C_IMG = transform.scale(image.load('assets/images/notes/c.png'), (50, 50))
D_IMG = transform.scale(image.load('assets/images/notes/d.png'), (50, 50))
E_IMG = transform.scale(image.load('assets/images/notes/e.png'), (50, 50))


A_IMG = E_IMG  
F_IMG = C_IMG  
G_IMG = D_IMG  
B_IMG = E_IMG  
H1_IMG = C_IMG  
H2_IMG = D_IMG  
H3_IMG = E_IMG  
H4_IMG = C_IMG  

NOTE_IMAGES = {
    'C': C_IMG,
    'D': D_IMG,
    'E': E_IMG,
    'F': F_IMG,
    'G': G_IMG,
    'A': A_IMG,
    'B': B_IMG,
    'H1': H1_IMG,
    'H2': H2_IMG,
    'H3': H3_IMG,
    'H4': H4_IMG,
}


_FLYING_NOTES = []

def spawn_flying_note(rect, note_name: Optional[str]):
    import random
    if not note_name:
        return
    img = NOTE_IMAGES.get(note_name)
    if not img:
        return
    
    
    x = rect.centerx - img.get_width() // 2 + random.randint(-10, 10)
    y = rect.y - img.get_height() - 10
    vy = random.uniform(-2.5, -1.5)  
    rotation = random.uniform(-15, 15)  
    
    _FLYING_NOTES.append({
        'img': img, 
        'x': x, 
        'y': y, 
        'vy': vy,
        'rotation': rotation,
        'alpha': 255,
        'scale': 1.0
    })

def update_and_draw_flying_notes(screen):
    import random
    to_remove = []
    for n in _FLYING_NOTES:
        
        n['y'] += n['vy']
        n['x'] += random.uniform(-0.5, 0.5)  
        
        
        if n['y'] < 200:
            n['alpha'] = max(0, n['alpha'] - 3)
            n['scale'] = max(0.7, n['scale'] - 0.005)
        
        
        if n['alpha'] > 0:
            
            img = n['img'].copy()
            
            
            if n['scale'] != 1.0:
                new_size = (int(img.get_width() * n['scale']), 
                           int(img.get_height() * n['scale']))
                img = transform.scale(img, new_size)
            
            
            img.set_alpha(n['alpha'])
            
            
            if n['rotation'] != 0:
                img = transform.rotate(img, n['rotation'])
            
            screen.blit(img, (n['x'], n['y']))
        
        
        if n['y'] + n['img'].get_height() < 0 or n['alpha'] <= 0:
            to_remove.append(n)
    
    for n in to_remove:
        _FLYING_NOTES.remove(n)

def draw_key_effect(screen, rect, is_pressed=False, note=None):
    if not is_pressed:
        base_color = (220, 220, 220)
    else:
        base_color = (170, 220, 255)

    draw.rect(screen, base_color, rect, border_radius=8)
    draw.rect(screen, BLACK, rect, 2, border_radius=8)

