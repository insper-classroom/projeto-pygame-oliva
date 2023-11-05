import pygame

def scale(lista_rect, tam_tela):
    
    tam_tela_orig = [1280, 720]
    if type(lista_rect) == list:
        new_val = []
        for rect in lista_rect:
            new_val += [pygame.Rect(rect.x/tam_tela_orig[0]*tam_tela[0], rect.y/tam_tela_orig[1]*tam_tela[1], 
                        rect.width/tam_tela_orig[0]*tam_tela[0], rect.height/tam_tela_orig[1]*tam_tela[1])]
            
    elif type(lista_rect) == dict:
        new_val = {}
        for key, rects in lista_rect.items():
            for rect in rects:
                try:
                    new_val[key] += [pygame.Rect(rect.x/tam_tela_orig[0]*tam_tela[0], rect.y/tam_tela_orig[1]*tam_tela[1], 
                                rect.width/tam_tela_orig[0]*tam_tela[0], rect.height/tam_tela_orig[1]*tam_tela[1])]
                except KeyError:
                    new_val[key] = [pygame.Rect(rect.x/tam_tela_orig[0]*tam_tela[0], rect.y/tam_tela_orig[1]*tam_tela[1], 
                                rect.width/tam_tela_orig[0]*tam_tela[0], rect.height/tam_tela_orig[1]*tam_tela[1])]
    return new_val