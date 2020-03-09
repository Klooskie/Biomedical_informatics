import vtk

# --- source: read data
dir = 'mr_brainixA'
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir)
reader.Update()
imageData = reader.GetOutput()

print(imageData.GetScalarRange())
print(imageData.GetDimensions())
# print(imageData)

# counter filter
counter_filter = vtk.vtkContourFilter()
counter_filter.SetInputConnection(reader.GetOutputPort())
counter_filter.SetNumberOfContours(1)
counter_filter.SetValue(0, 100)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(counter_filter.GetOutputPort())
mapper.SetColorModeToMapScalars()

# color transfer function
ctf = vtk.vtkColorTransferFunction()
ctf.AddRGBPoint(1, 1, 0, 0)
ctf.AddRGBPoint(300, 0, 1, 0)
ctf.AddRGBPoint(600, 0, 0, 1)
mapper.SetLookupTable(ctf)

# actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# --- renderer
ren1 = vtk.vtkRenderer()
ren1.SetBackground(0, 0, 0)
ren1.AddActor(actor)

# --- window
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1)
renWin.SetSize(800, 600)

# --- interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# --- slider to change frame: callback class, sliderRepresentation, slider
class FrameCallback(object):
    def __init__(self, actor, renWin):
        self.renWin = renWin
        self.actor = actor

    def __call__(self, caller, ev):
        value = caller.GetSliderRepresentation().GetValue()
        counter_filter.SetValue(0, int(value))
        self.renWin.Render()


sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(.7, .1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(.9, .1)
sliderRep.SetMinimumValue(0)
sliderRep.SetMaximumValue(1715)
sliderRep.SetValue(100)
sliderRep.SetTitleText("iso value")

slider = vtk.vtkSliderWidget()
slider.SetInteractor(iren)
slider.SetRepresentation(sliderRep)
slider.SetAnimationModeToAnimate()
slider.EnabledOn()
slider.AddObserver('InteractionEvent', FrameCallback(actor, renWin))

# --- run
style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)
iren.Initialize()
iren.Start()
