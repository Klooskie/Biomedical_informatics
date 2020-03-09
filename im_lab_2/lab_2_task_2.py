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

# mapper
mapper = vtk.vtkSmartVolumeMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# actor
actor = vtk.vtkVolume()
actor.SetMapper(mapper)

piecewiseFunction = vtk.vtkPiecewiseFunction()
piecewiseFunction.AddPoint(100, 0.0)
piecewiseFunction.AddPoint(300, 0.2)
piecewiseFunction.AddPoint(500, 0.0)
actor.GetProperty().SetScalarOpacity(0, piecewiseFunction)

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

        new_piecewise_function = vtk.vtkPiecewiseFunction()
        new_piecewise_function.AddPoint(int(value) - 200, 0.0)
        new_piecewise_function.AddPoint(int(value), 0.2)
        new_piecewise_function.AddPoint(int(value) + 200, 0.0)
        actor.GetProperty().SetScalarOpacity(0, new_piecewise_function)

        self.renWin.Render()


sliderRep = vtk.vtkSliderRepresentation2D()
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(.7, .1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(.9, .1)
sliderRep.SetMinimumValue(0)
sliderRep.SetMaximumValue(1715)
sliderRep.SetValue(300)
sliderRep.SetTitleText("transfer function")

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
