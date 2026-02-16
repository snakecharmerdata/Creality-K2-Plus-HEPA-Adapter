
import FreeCAD
import Part

def create_hepa_filter_holder():
    """
    This function creates a 3D model of a HEPA filter holder based on provided specifications.
    The script is intended to be run in FreeCAD.
    """
    
    # --- Part 1: Build the Frame ---
    
    # B) Create OUTER (the outer frame block)
    # Dimensions: 118.50 (X) x 20.00 (Y) x 82.20 (Z)
    outer_frame = Part.makeBox(118.50, 20.00, 82.20)
    
    # C) Create INNER (the hole to subtract)
    # Dimensions: 108.88 (X) x 20.00 (Y) x 72.20 (Z)
    inner_hole = Part.makeBox(108.88, 20.00, 72.20)
    
    # Position INNER to be centered inside OUTER
    inner_hole.translate(FreeCAD.Vector(4.81, 0.00, 5.00))
    
    # D) Cut INNER from OUTER to make the frame
    frame = outer_frame.cut(inner_hole)
    
    # --- Part 2: Add Magnet Chambers and Bores ---
    
    # A) Create LEFT boss (solid cylinder)
    # Radius = 13.10, Height = 10.00
    left_boss = Part.makeCylinder(13.10, 10.00)
    # Placement: Rotate -90 deg around X-axis, then translate
    left_boss.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
    left_boss.translate(FreeCAD.Vector(-10.30, 10.00, 41.10))
    
    # B) Create RIGHT boss (solid cylinder)
    # Same dimensions and rotation as the left boss
    right_boss = Part.makeCylinder(13.10, 10.00)
    right_boss.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
    right_boss.translate(FreeCAD.Vector(128.80, 10.00, 41.10))
    
    # C) Fuse bosses with the frame
    frame_with_bosses = frame.fuse(left_boss).fuse(right_boss)
    
    # D) Create LEFT bore (hole cylinder)
    # Radius = 10.30, Height = 10.00
    left_bore = Part.makeCylinder(10.30, 10.00)
    # Placement: Rotate -90 deg around X-axis, then translate
    # Y position is 9.00 to leave a 1.00mm back cap (since boss Y is 10.00 and bore height is 10.00)
    left_bore.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
    left_bore.translate(FreeCAD.Vector(-10.30, 9.00, 41.10))

    # E) Create RIGHT bore (hole cylinder)
    # Same dimensions and rotation as the left bore
    right_bore = Part.makeCylinder(10.30, 10.00)
    right_bore.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), -90)
    right_bore.translate(FreeCAD.Vector(128.80, 9.00, 41.10))
    
    # F) Cut the bores from the fused frame
    final_part = frame_with_bosses.cut(left_bore).cut(right_bore)
    
    return final_part

if __name__ == "__main__":
    # This block will run when the script is executed in FreeCAD
    
    # Ensure a document is active
    if not FreeCAD.ActiveDocument:
        FreeCAD.newDocument("HepaFilterHolder")
    
    # Create the part
    hepa_holder = create_hepa_filter_holder()
    
    # Add the final part to the document
    Part.show(hepa_holder)
    
    # Recompute the document and fit the view
    FreeCAD.ActiveDocument.recompute()
    if FreeCAD.GuiUp:
        FreeCAD.Gui.activeDocument().activeView().fitAll()

    print("HEPA Filter Holder script finished successfully.")
    print("The final part has been created in the active document.")
    print("To export, select the created object and go to File > Export... and choose STL Mesh.")
