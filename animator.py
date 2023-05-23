import bpy

#Every object in the scene is named a number
#if the frame number is higher than the object number, the object is visible

#for every object in the scene
for obj in bpy.data.objects:
    #get the object number from the object name
    obj_num = int(obj.name)
    #create driver for the object's visibility
    d = obj.driver_add('hide_render')
    #driver = obj_nun > frame_number
    d.driver.expression = str(obj_num) + ' > frame'
    
    #copy the driver to the viewport visibility
    d2 = obj.driver_add('hide_viewport')
    d2.driver.expression = str(obj_num) + ' > frame'
