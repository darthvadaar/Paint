#Sherlock Paint - Sid Bedekar
#This paint program allows to user to use basic and some advanced tools to create artwork. Basic tools include: pencil, eraser, brush.
#Additional capabilities such as music are also available.
from pygame import *
from random import *
from math import *

screen = display.set_mode((1366,768,))                     
#Tool_menu_variables_
col = (0,0,0)
toolboxpos = []
toollist = ["pencil","eraser","brush","line","square","circle","fill","spray","colpicker","stamp"]
tool = toollist[0]
desctitle = ["Pencil:","Eraser:","Brush:","Line:","Rectangle:","Ellipse:","Fill:","Spray:","Eyedrop tool:","Stamp:"]    #Tools description
desc1 = ["Write down clues you" , "Erase incorrect" , "Paint clues to" , "Draw straight lines." , "Draw rectangles. Left" , "Draw Ellipse. Left" , "Fill an area with" , "Draw a spraypaint","Left click to equip the","Stamp images. Scroll"]
desc2 = ["may encounter in ","deductions.","understand their","","click for filled and","click for filled and","the selected colour.","effect with the chosen","colour which is under ","to change image."]
desc3 = ["your investigations."," ","morphology.","","Right click for unfilled.","Right click for unfilled.","","colour.","your mouse.",""]
desc4 = ["","","","","Middle click for square.","Middle click for circle.","","","","",""]

#pencil/eraser/brush variables_
penposlist = []
width = 5
oldpos = []

#Layout_draw
boxcol = (255,255,255)
screen.blit(image.load("back.png"),(0,0))   #Background draw
canvasrect = draw.rect(screen,(255,255,255),(200,100,1000,600))      #canvas draw
canvas = screen.subsurface(canvasrect)

#Font Settings
font.init()
desc_font = font.SysFont("kaiti", 12)

#Save/Undo/Redo Box (Controls)
control_desc = ["Save Canvas (name.ext)","Load Canvas (name.ext)","Undo","Redo","Clear canvas"]
control_pics = [image.load("save.png"),image.load("load.png"),image.load("undo.png"),image.load("redo.png"),image.load("clear.png")]
control_actions = ["save","load","undo","redo","clear"]
picnum = 0
control_box = []
for x in range (20,141,30):
    control_box.append(draw.rect(screen,(255,255,255),(x,70,25,25)))    #rects and pics for controls
    screen.blit(control_pics[picnum],(x,70))
    picnum += 1
control = "none"
saveload_input = ""     #text that is turned into image (for save control)
undo_list = [canvas.copy()] #always has a blank canvas so you can undo until a blank canvas
redo_list = []

#Music Variables
mixer.init()
music_rectlist = []
music_control_icons = [image.load("pause_button.png"),image.load("play_button.png")]
for x in range (1100,1205,35):
    music_rect = draw.rect(screen,(255,255,255),(x,700,30,30))      #Draws the music boxes
    screen.blit(image.load("music_icon.jpg"),(x,700))
    music_rectlist.append(music_rect)
music_control = []
for x in range (1100,1136,35):
    music_control.append(draw.rect(screen,(255,255,255),(x,735,30,30)))

#fill list
fill_list = []

#text tool vars
typing = False
typing_text = ""

#Stamps
stamplist = [image.load("stamp1.png"),image.load("stamp2.png"),image.load("stamp3.png"),image.load("stamp4.png"),image.load("stamp5.png"),image.load("stamp6.png"),image.load("stamp7.png"),image.load("stamp8.png")]
preview_stamplist = [image.load("p_stamp1.png"),image.load("p_stamp2.png"),image.load("p_stamp3.png"),image.load("p_stamp4.png"),image.load("p_stamp5.png"),image.load("p_stamp6.png"),image.load("p_stamp7.png"),image.load("p_stamp8.png")] 
stampnum = 0    #stamp number from the lists
stamp_x = [30,29,44,47,69,31,25,54] #locations of stamps (to get stamps in the center of the mouse while blitting)
stamp_y = [100,100,100,100,100,100,19,125]

#background vars
back = [image.load("background1.png"),image.load("background2.jpg"),image.load("background3.jpg"),image.load("background4.jpg"),image.load("background5.png")]
backnum = 0
back_box = []
for y in range (210,735,105):
    back_box.append(draw.rect(screen,(255,255,255),(1210,y,150,100)))
    screen.blit(transform.scale(back[backnum],(150,100)),(1210,y,150,100))
    backnum += 1

#tab buttons
tab_list = []
tab_rect = (20,100,130,340)
tab_status = 0
tabnum = 0
for i in range(100,170,35):
    tab_list.append(draw.rect(screen,(255,255,255),(155,i,30,30)))

running = True
while running :
    for e in event.get():               #event loop
        if e.type == MOUSEBUTTONDOWN:   #varables for square, line and circle tool
            canvascopy = canvas.copy()  
            shape_oldx = canvas_mx
            shape_oldy = canvas_my
            if tool == "stamp":
                if e.button == 4:       #mouse wheel up
                    stampnum += 1       #changes what stamp is selected   
                    if stampnum > 7:
                            stampnum = 7
                
                if e.button == 5:       #mouse wheel down
                    stampnum -= 1
                    if stampnum < 0:
                            stampnum = 0
            else:
                if e.button == 4:       #mouse wheel up
                    width += 2          #Changes the width of the tool being used (except pencil)
                    if width > 75:
                            width = 70
                
                if e.button == 5:       #mouse wheel down
                    width -= 2
                    if width < 2:
                            width = 2
                    
        if control == "save" or control == "load":
            draw.rect(screen,(255,255,255),(0,0,150,20))
            if e.type == KEYDOWN:
                if e.key == K_BACKSPACE:  #remove last letter if backspace
                    saveload_input = saveload_input[:-1]
                elif e.key == K_RETURN:
                    if saveload_input.count(".png") == 0 or saveload_input.count(".jpg") == 0 or saveload_input.count(".jpeg") == 0 :
                        saveload_input += ".png"    #if no extension, saves as png 
                    if control == "save":
                        image.save(canvas, saveload_input)  #saves if save is selected
                        control = "none"
                    elif control == "load":
                        loadimage = image.load(saveload_input)#loads if load is selected
                        if canvas.get_width != 1000 or canvas.get_height != 600:
                            loadimage = transform.scale(loadimage,(1000,600))  #resize image if > or < (1000,600)
                        screen.blit(loadimage,(200,100))
                        control = "none"
                    draw.rect(screen,(0,0,0),(0,0,150,20))
                    saveload_input = ""
                elif e.key == K_ESCAPE:
                    draw.rect(screen,(0,0,0),(0,0,150,20))
                    saveload_input = ""
                    control = "none"
                elif e.unicode:         #checks for characters last because dont want to add a backspace/return key to saveload_input
                    if len(saveload_input) < 20:    #checks if under 20 characters
                        saveload_input += e.unicode #records what the filename will be

        if canvasrect.collidepoint(mouse.get_pos()) and e.type == MOUSEBUTTONUP:           #appends the canvas into undo_list everytime mouse is released   
            undo_list.append(canvas.copy())

        if control_box[2].collidepoint(mouse.get_pos()) and e.type == MOUSEBUTTONDOWN and len(undo_list) > 1:
            canvas.blit(undo_list[-2],(0,0))  #blits the second last screen from the list
            redo_list.append(undo_list[- 1]) #add to redo list before removing the recent canvas
            del[undo_list[- 1]]  #deletes the most recent canvas in list
            control = "none"
            
        if control_box[3].collidepoint(mouse.get_pos()) and e.type == MOUSEBUTTONDOWN and len(redo_list) !=  0:
            canvas.blit(redo_list[-1],(0,0))
            undo_list.append(redo_list[-1])     #puts back into undo list so you can undo the redo
            del[redo_list[- 1]]  #deletes the most recent canvas in list
            control = "none"

        for i in range(0,2):
            if tab_list[i].collidepoint(mouse.get_pos()) and e.type == MOUSEBUTTONDOWN :                  #draws tab boxes
                tabnum = i
                tab_status = i
                if i == 0:
                    pass

        if tool == "fill":                         #fill
            if e.type == MOUSEBUTTONDOWN and canvasrect.collidepoint(mpos) :
                canvas.set_clip(canvasrect)
                startcol = canvas.get_at((canvas_mx,canvas_my))
                fill_list.append((canvas_mx,canvas_my))
                while (len(fill_list)) > 0:
                    startx,starty = fill_list.pop(0)
                    if canvas.get_at((startx,starty)) == startcol:
                        canvas.set_at((startx,starty),col)
                        fill_list.append((startx,starty - 1))
                        fill_list.append((startx, starty + 1))
                        fill_list.append((startx + 1, starty))
                        fill_list.append((startx - 1, starty))
                canvas.set_clip(None)

        if tool == "text":
            if e.type == MOUSEBUTTONDOWN and e.button == 1 and canvasrect.collidepoint(mpos):
                canvas_text = canvas.copy()
                mx , my= mouse.get_pos()
                text_pos = (mx-200, my - 100)
                typing = True
            if typing:
                if e.type == KEYDOWN:
                    if e.key == K_BACKSPACE:
                        typing_text = typing_text[:-1]
                    elif e.key == K_RETURN:
                        typing = False
                    elif  e.unicode:
                        typing_text += e.unicode
            elif typing == False:
                typing_text = ""
             
        if e.type == QUIT:
            running = False

#_____________________________________________________
    mpos = mouse.get_pos()
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    canvas_mx = mx - 200        #mouse position relative to subsurface: canvas (x)...
    canvas_my = my - 100        #...(y)
    canvas_mpos = (canvas_mx,canvas_my)
    stamp = stamplist[stampnum]
    texttool_font = font.SysFont("kaiti", width)
    
    
    screen.blit(music_control_icons[0],(1100,735))  # music control icon blit
    screen.blit(music_control_icons[1],(1136,735))
   
    for boxx in range (20,140,70):                                          #tool boxes draw
        for boxy in range (100,420,70):
            toolboxpos.append(draw.rect(screen,boxcol,(boxx,boxy,60,60)))
    
    if tab_status == 0:
        toollist = ["pencil","eraser","brush","line","square","circle","fill","spray","colpicker","stamp"]
        desctitle = ["Pencil:","Eraser:","Brush:","Line:","Rectangle:","Ellipse:","Fill:","Spray:","Eyedrop tool:","Stamp:"]    #Tools description tab 1
        desc1 = ["Write down clues you" , "Erase incorrect" , "Paint clues to" , "Draw straight lines." , "Draw rectangles. Left" , "Draw Ellipse. Left" , "Fill an area with" , "Draw a spraypaint","Left click to equip the","Stamp images. Scroll"]
        desc2 = ["may encounter in ","deductions.","understand their","","click for filled and","click for filled and","the selected colour.","effect with the chosen","colour which is under ","to change image."]
        desc3 = ["your investigations."," ","morphology.","","Right click for unfilled.","Right click for unfilled.","","colour.","your mouse.",""]
        desc4 = ["","","","","Middle click for square.","Middle click for circle.","","","","",""]
    elif tab_status == 1:
        toollist = ["text","","","","","","","","",""]
        desctitle = ["Text Tool:","","","","","","","","",""]    #Tools description tab 2
        desc1 = ["Use if your hand writing" , "" , "" , "" , "" , "" , "" , "","",""]
        desc2 = ["is disgusting. Left click","","","","","","",""," ",""]
        desc3 = ["to start typing"," ","","","","","","","",""]
        desc4 = ["and enter to stop.","","","","","","","","","",""]
            
    draw.rect(screen,(255,255,255),(20,450,165,100),0)                      #Description text Box Draw
    for i in range (0,10): 
        if tool == toollist[i] or toolboxpos[i].collidepoint(mpos):          #Prints text in description box if hovering over a tool
            screen.blit(desc_font.render(desctitle[i], True, (255,0,0)),(25,455))
            screen.blit(desc_font.render(desc1[i], True, (255,0,0)),(25,470))
            screen.blit(desc_font.render(desc2[i], True, (255,0,0)),(25,485))
            screen.blit(desc_font.render(desc3[i], True, (255,0,0)),(25,500))
            screen.blit(desc_font.render(desc4[i], True, (255,0,0)),(25,515))
            if mb[0] == 1:                                                  #Tool Selection
                tool = toollist[i]
                
    draw.rect(screen,(255,255,255),(1210,100,100,100),0)                     #Preview Box draw
    if tool == "stamp":
        screen.blit(preview_stamplist[stampnum],(1210,100))                  #Draws what sticker is currently selected
    else:       
        draw.circle(screen,(col),(1260,150),int(width/2))                   #Brush size and colour

    colimage  = screen.blit(image.load("colselect.png"),(5,585))            #Colour palette draw
    if colimage.collidepoint(mpos) and mb[0] == 1:                          #Colour palette mouse
        col = screen.get_at((mpos))

    if music_rectlist[0].collidepoint(mpos) and mb[0] == 1:                 #Music play
        mixer.music.load("music/sherlock 1.wav")
        mixer.music.play()
    elif music_rectlist[1].collidepoint(mpos) and mb[0] == 1:
        mixer.music.load("music/sherlock 2.wav")
        mixer.music.play()
    elif music_rectlist[2].collidepoint(mpos) and mb[0] == 1:
        mixer.music.load("music/sherlock 3.wav")
        mixer.music.play()
    if music_control[0].collidepoint(mpos) and mb[0] == 1:
        mixer.music.pause()
    elif music_control[1].collidepoint(mpos) and mb[0] == 1:
        mixer.music.unpause()

    for i in range(0,5):
        if control_box[i].collidepoint(mpos):                              #control description
            screen.blit(desc_font.render(control_desc[i],True,(255,0,0)),(25,455))
            if mb[0] == 1:
                control = control_actions[i]    #control selection

    for i in range(0,5):
        if back_box[i].collidepoint(mpos) and mb[0] == 1:
            canvas.blit(back[i],(0,0))
    if tab_status == 0:
        if tool == "pencil":
            screen.blit(image.load("s_pencil.png"),(20,100))    #Selected tool icon
        else:
            screen.blit(image.load("pencil.png"),(20,100))      #unselected tool icons
        if tool == "eraser":
            screen.blit(image.load("s_eraser.png"),(20,170))
        else:
            screen.blit(image.load("eraser.png"),(20,170))                          
        if tool == "brush":
            screen.blit(image.load("s_brush.png"),(20,240))
        else:
            screen.blit(image.load("brush.png"),(20,240))
        if tool == "line":
            screen.blit(image.load("s_line.png"),(20,310))
        else:
            screen.blit(image.load("line.png"),(20,310))
        if tool == "square":
            screen.blit(image.load("s_square.png"),(20,380))
        else:
            screen.blit(image.load("square.png"),(20,380)) 
        if tool == "circle":
            screen.blit(image.load("s_circle.png"),(90,100))
        else :
            screen.blit(image.load("circle.png"),(90,100)) 
        if tool == "fill":
            screen.blit(image.load("s_fill.png"),(90,170))
        else:
            screen.blit(image.load("fill.png"),(90,170))
        if tool == "spray":
            screen.blit(image.load("s_spray.png"),(90,240))
        else:
            screen.blit(image.load("spray.png"),(90,240)) 
        if tool == "colpicker":
            screen.blit(image.load("s_colpicker.png"),(90,310))
        else:
            screen.blit(image.load("colpicker.png"),(90,310))
        if tool == "stamp":
            screen.blit(image.load("s_stamp.png"),(90,380))
        else:
            screen.blit(image.load("stamp.png"),(90,380))
    elif tab_status == 1:
        if tool == "text":
            screen.blit(image.load("s_texttool_icon.png"),(20,100))
        else:
            screen.blit(image.load("texttool_icon.png"),(20,100))


#----------Controls(save/load/undo/redo/none[no controls in use])------------#

    if control == "save" or control == "load":
        saveload_input_pic = desc_font.render(saveload_input,True,(255,0,0)) #the saveload_input text is turned into picture
        screen.blit(saveload_input_pic , (0,0))     #blits saveload_input_pic 
    elif control == "clear":
        canvas == draw.rect(canvas,(255,255,255),(0,0,1000,600))
        control ="none"
    if len(undo_list) > 150:     #if more than 150 screens in list, removes the fist item in the list (for undo and redo, to prevent lagging or crash.)
        del[undo_list[0]]
    if len(redo_list) > 150:
        del[redo_list[0]]           

#------------------------------Tool Selection--------------------------------#

    if tool == "text" and typing:
        typing_text_pic = texttool_font.render(typing_text, True, (col))
        canvas.blit(canvas_text,(0,0))
        canvas.blit(typing_text_pic,text_pos)

    mouse.set_visible(True)
    if canvasrect.collidepoint(mpos):
        if tool == "pencil" and mb[0] == 1:                         # Pencil
            mouse.set_visible(False)
            oldpos.append(canvas_mpos)
            if len(oldpos) > 2:         #two points stored and connected
                del oldpos[0]           #no more than 2 points at a time
            draw.line(canvas,(col),(oldpos[0]),(canvas_mpos),1)
        
        elif tool == "eraser" and mb[0] == 1:                       # Eraser
            mouse.set_visible(False)
            oldpos.append(canvas_mpos)
            if len(oldpos) > 2:
                del oldpos[0]
                draw.line(canvas,(255,255,255),(oldpos[0]),(canvas_mpos),width)
                draw.circle(canvas,(255,255,255),(canvas_mpos),int(width/2))
                
        elif tool == "brush" and mb[0] == 1:                        # Brush
            mouse.set_visible(False)
            oldpos.append(canvas_mpos)
            draw.circle(canvas,col,(oldpos[0]),int((width/2) - 1))
            if len(oldpos) > 2:
                del oldpos[0]
            draw.line(canvas,(col),(oldpos[0]),(canvas_mpos),width)

        elif tool == "line":                                        #Line Tool
            if mb[0] == 1:
                mouse.set_visible(False)
                canvas.blit(canvascopy,(0,0))
                draw.circle(canvas,(col),(shape_oldx,shape_oldy),int((width/2) - 1)) #Gets rid of rough edges
                draw.circle(canvas,(col),(canvas_mpos),int((width/2) - 1))                 #Gets rid of rough edges
                draw.line(canvas,col,(shape_oldx,shape_oldy),(canvas_mpos),width)
                                    
        elif tool == "square":                                      #Square Tool
            if mb[0] == 1:  #left click = filled rectangle
                mouse.set_visible(False)
                canvas.blit(canvascopy,(0,0)) 
                draw.rect(canvas,col,(shape_oldx, shape_oldy, canvas_mx - shape_oldx, canvas_my - shape_oldy),0)
            elif mb[1] == 1:
                mouse.set_visible(False)
                canvas.blit(canvascopy,(0,0))   #middle click = square
                draw.rect(canvas,col,(shape_oldx, shape_oldy, canvas_mx - shape_oldx, canvas_mx - shape_oldx),0)
            elif mb[2] == 1:    #right click = unfilled rectangle
                mouse.set_visible(False)
                canvas.blit(canvascopy,(0,0))
                draw.rect(canvas,col,(shape_oldx, shape_oldy, canvas_mx - shape_oldx, canvas_my - shape_oldy),width)

        elif tool == "circle":                                      #Circle Tool
            circle_x = canvas_mx - shape_oldx
            circle_y = canvas_my - shape_oldy
            ellipserect = Rect(canvas_mx, canvas_my,  shape_oldx - canvas_mx,  shape_oldy - canvas_my)
            ellipserect.normalize()
            if mb[0] == 1 :  #left click = filled ellipse
                mouse.set_visible(False)
                canvas.blit(canvascopy,(0,0))
                draw.ellipse(canvas,col,ellipserect,0)
            elif mb[1] == 1:    #middle click = circle
                mouse.set_visible(False)
                dist = int(sqrt(abs((shape_oldx - canvas_mx)**2 + (shape_oldy - canvas_my)**2)))
                canvas.blit(canvascopy,(0,0))
                draw.circle(canvas , col , (shape_oldx , shape_oldy) , dist)
            elif mb[2] == 1:    #right click = unfilled ellipse
                mouse.set_visible(False)
                elip_x = ellipserect.width // 2
                elip_y = ellipserect.height // 2
                if elip_x > width and elip_y > width:
                    canvas.blit(canvascopy,(0,0))
                    draw.ellipse(canvas,col,ellipserect,width)
                else:
                    canvas.blit(canvascopy,(0,0))
                    draw.ellipse(canvas,col,ellipserect)       
            
        elif tool == "colpicker" and mb[0] == 1:
            mouse.set_visible(False)
            col = screen.get_at((mpos))                             #colour picker
                         
        elif tool == "spray" and mb[0] == 1:                         #Spray
            for i in range(10): #spray_tool_variables
                mouse.set_visible(False)
                rangex = randint(canvas_mx - width,canvas_mx + width) #Gets a range for x values
                rangey = randint(canvas_my-width,canvas_my + width) #Gets a range for y values
                dist_spray = sqrt(abs((canvas_mx-rangex)**2 + (canvas_my-rangey)**2))   #Gets distance (dist_spray from mpos to width of circle)
                if mb[0] == 1 and dist_spray <= width:      
                    canvas.set_at((rangex,rangey),col)

        elif tool == "stamp" and mb[0] == 1:                        #Stamp tool
            mouse.set_visible(False)
            canvas.blit(canvascopy,(0,0))
            canvas.blit(stamp,(canvas_mx - stamp_x[stampnum], canvas_my - stamp_y[stampnum]))
            
        elif 1 not in mb:
            oldpos = []
            
    
#_______________________________________
    display.flip()
quit()
