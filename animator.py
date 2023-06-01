import bpy

#Every object in the scene is named a number
#if the frame number is higher than the object number, the object is visible

#for every object in the scene
def anim(obj, i, single_frame=False):
    #create driver for the object's visibility
    d = obj.driver_add('hide_render')
    #driver = obj_nun > frame_number
    if single_frame:
        fr = '== frame'
    else:
        fr = '> frame'
    d.driver.expression = str(i) + fr
    
    #copy the driver to the viewport visibility
    d2 = obj.driver_add('hide_viewport')
    d2.driver.expression = str(i) + fr
