
import vtk

from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkCommonMath import vtkRungeKutta4
from vtkmodules.vtkFiltersSources import vtkPointSource, vtkArrowSource
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersCore import vtkTubeFilter, vtkStructuredGridOutlineFilter, vtkGlyph3D
from vtkmodules.vtkRenderingCore import vtkPolyDataMapper, vtkActor, vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor, vtkCamera
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter

from vtk.util.misc import vtkGetDataRoot
from vtk.util.colors import *

import numpy as np
VTK_DATA_ROOT = vtkGetDataRoot()

# We read a data file the is a CFD analysis of airflow in an office
# (with ventilation and a burning cigarette). We force an update so
# that we can query the output for its length, i.e., the length of the
# diagonal of the bounding box. This is useful for normalizing the
# data.
reader = vtkXMLStructuredGridReader()
reader.SetFileName("stream-data.vts")
reader.Update()

length = reader.GetOutput().GetLength()

maxVelocity =reader.GetOutput().GetPointData().GetVectors().GetMaxNorm()
maxTime = 35.0*length/maxVelocity



#creating streamline
integ = vtkRungeKutta4()



pointSource = vtkPointSource()
pointSource.SetNumberOfPoints(6)
pointSource.SetCenter(2.31, 1.63, 0.53)  
pointSource.SetRadius(1.075) 


# Get the points generated by the vtkPointSource
pointSource.Update()
seedPoints = pointSource.GetOutput()


##########################################################################


streamer = vtkStreamTracer()

streamer.SetInputConnection(reader.GetOutputPort())
streamer.SetSourceData(seedPoints)
streamer.SetIntegrator(integ)
streamer.SetStartPosition(0.2, 0.2, 0.2)
streamer.SetIntegrationDirectionToBoth()
streamer.SetMaximumPropagation(500)
initialStep = 0.1  #inititalintegrations step
streamer.SetInitialIntegrationStep(initialStep) 

streamTube = vtkTubeFilter()
streamTube.SetInputConnection(streamer.GetOutputPort())

streamTube.SetRadius(0.02)
streamTube.SetNumberOfSides(12)

mapStreamTube = vtkPolyDataMapper()
mapStreamTube.SetInputConnection(streamTube.GetOutputPort())
mapStreamTube.SetScalarRange(reader.GetOutput().GetPointData().GetScalars().GetRange())
streamTubeActor = vtkActor()
streamTubeActor.SetMapper(mapStreamTube)
streamTubeActor.GetProperty().BackfaceCullingOn()


#### Insert your code here for vector filed visualization using vtkGlyph3D ####

arrowSource = vtkArrowSource()


glyph = vtk.vtkGlyph3D()
glyph.SetInputConnection(reader.GetOutputPort())
glyph.SetSourceConnection(arrowSource.GetOutputPort())

glyph.SetScaleModeToScaleByVector()

glyphMapper = vtk.vtkPolyDataMapper()
glyphMapper.SetInputConnection(glyph.GetOutputPort())

glyphActor = vtkActor()
glyphActor.SetMapper(glyphMapper)

################################################################################
# From here on we generate a whole bunch of planes which correspond to
# the geometry in the analysis; tables, bookshelves and so on.
table1 = vtkStructuredGridGeometryFilter()
table1.SetInputConnection(reader.GetOutputPort())
table1.SetExtent(11, 15, 7, 9, 8, 8)
mapTable1 = vtkPolyDataMapper()
mapTable1.SetInputConnection(table1.GetOutputPort())
mapTable1.ScalarVisibilityOff()
table1Actor = vtkActor()
table1Actor.SetMapper(mapTable1)
table1Actor.GetProperty().SetColor(.59, .427, .392)

table2 = vtkStructuredGridGeometryFilter()
table2.SetInputConnection(reader.GetOutputPort())
table2.SetExtent(11, 15, 10, 12, 8, 8)
mapTable2 = vtkPolyDataMapper()
mapTable2.SetInputConnection(table2.GetOutputPort())
mapTable2.ScalarVisibilityOff()
table2Actor = vtkActor()
table2Actor.SetMapper(mapTable2)
table2Actor.GetProperty().SetColor(.59, .427, .392)

FilingCabinet1 = vtkStructuredGridGeometryFilter()
FilingCabinet1.SetInputConnection(reader.GetOutputPort())
FilingCabinet1.SetExtent(15, 15, 7, 9, 0, 8)
mapFilingCabinet1 = vtkPolyDataMapper()
mapFilingCabinet1.SetInputConnection(FilingCabinet1.GetOutputPort())
mapFilingCabinet1.ScalarVisibilityOff()
FilingCabinet1Actor = vtkActor()
FilingCabinet1Actor.SetMapper(mapFilingCabinet1)
FilingCabinet1Actor.GetProperty().SetColor(.8, .8, .6)

FilingCabinet2 = vtkStructuredGridGeometryFilter()
FilingCabinet2.SetInputConnection(reader.GetOutputPort())
FilingCabinet2.SetExtent(15, 15, 10, 12, 0, 8)
mapFilingCabinet2 = vtkPolyDataMapper()
mapFilingCabinet2.SetInputConnection(FilingCabinet2.GetOutputPort())
mapFilingCabinet2.ScalarVisibilityOff()
FilingCabinet2Actor = vtkActor()
FilingCabinet2Actor.SetMapper(mapFilingCabinet2)
FilingCabinet2Actor.GetProperty().SetColor(.8, .8, .6)

bookshelf1Top = vtkStructuredGridGeometryFilter()
bookshelf1Top.SetInputConnection(reader.GetOutputPort())
bookshelf1Top.SetExtent(13, 13, 0, 4, 0, 11)
mapBookshelf1Top = vtkPolyDataMapper()
mapBookshelf1Top.SetInputConnection(bookshelf1Top.GetOutputPort())
mapBookshelf1Top.ScalarVisibilityOff()
bookshelf1TopActor = vtkActor()
bookshelf1TopActor.SetMapper(mapBookshelf1Top)
bookshelf1TopActor.GetProperty().SetColor(.8, .8, .6)

bookshelf1Bottom = vtkStructuredGridGeometryFilter()
bookshelf1Bottom.SetInputConnection(reader.GetOutputPort())
bookshelf1Bottom.SetExtent(20, 20, 0, 4, 0, 11)
mapBookshelf1Bottom = vtkPolyDataMapper()
mapBookshelf1Bottom.SetInputConnection(bookshelf1Bottom.GetOutputPort())
mapBookshelf1Bottom.ScalarVisibilityOff()
bookshelf1BottomActor = vtkActor()
bookshelf1BottomActor.SetMapper(mapBookshelf1Bottom)
bookshelf1BottomActor.GetProperty().SetColor(.8, .8, .6)

bookshelf1Front = vtkStructuredGridGeometryFilter()
bookshelf1Front.SetInputConnection(reader.GetOutputPort())
bookshelf1Front.SetExtent(13, 20, 0, 0, 0, 11)
mapBookshelf1Front = vtkPolyDataMapper()
mapBookshelf1Front.SetInputConnection(bookshelf1Front.GetOutputPort())
mapBookshelf1Front.ScalarVisibilityOff()
bookshelf1FrontActor = vtkActor()
bookshelf1FrontActor.SetMapper(mapBookshelf1Front)
bookshelf1FrontActor.GetProperty().SetColor(.8, .8, .6)

bookshelf1Back = vtkStructuredGridGeometryFilter()
bookshelf1Back.SetInputConnection(reader.GetOutputPort())
bookshelf1Back.SetExtent(13, 20, 4, 4, 0, 11)
mapBookshelf1Back = vtkPolyDataMapper()
mapBookshelf1Back.SetInputConnection(bookshelf1Back.GetOutputPort())
mapBookshelf1Back.ScalarVisibilityOff()
bookshelf1BackActor = vtkActor()
bookshelf1BackActor.SetMapper(mapBookshelf1Back)
bookshelf1BackActor.GetProperty().SetColor(.8, .8, .6)

bookshelf1LHS = vtkStructuredGridGeometryFilter()
bookshelf1LHS.SetInputConnection(reader.GetOutputPort())
bookshelf1LHS.SetExtent(13, 20, 0, 4, 0, 0)
mapBookshelf1LHS = vtkPolyDataMapper()
mapBookshelf1LHS.SetInputConnection(bookshelf1LHS.GetOutputPort())
mapBookshelf1LHS.ScalarVisibilityOff()
bookshelf1LHSActor = vtkActor()
bookshelf1LHSActor.SetMapper(mapBookshelf1LHS)
bookshelf1LHSActor.GetProperty().SetColor(.8, .8, .6)

bookshelf1RHS = vtkStructuredGridGeometryFilter()
bookshelf1RHS.SetInputConnection(reader.GetOutputPort())
bookshelf1RHS.SetExtent(13, 20, 0, 4, 11, 11)
mapBookshelf1RHS = vtkPolyDataMapper()
mapBookshelf1RHS.SetInputConnection(bookshelf1RHS.GetOutputPort())
mapBookshelf1RHS.ScalarVisibilityOff()
bookshelf1RHSActor = vtkActor()
bookshelf1RHSActor.SetMapper(mapBookshelf1RHS)
bookshelf1RHSActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2Top = vtkStructuredGridGeometryFilter()
bookshelf2Top.SetInputConnection(reader.GetOutputPort())
bookshelf2Top.SetExtent(13, 13, 15, 19, 0, 11)
mapBookshelf2Top = vtkPolyDataMapper()
mapBookshelf2Top.SetInputConnection(bookshelf2Top.GetOutputPort())
mapBookshelf2Top.ScalarVisibilityOff()
bookshelf2TopActor = vtkActor()
bookshelf2TopActor.SetMapper(mapBookshelf2Top)
bookshelf2TopActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2Bottom = vtkStructuredGridGeometryFilter()
bookshelf2Bottom.SetInputConnection(reader.GetOutputPort())
bookshelf2Bottom.SetExtent(20, 20, 15, 19, 0, 11)
mapBookshelf2Bottom = vtkPolyDataMapper()
mapBookshelf2Bottom.SetInputConnection(bookshelf2Bottom.GetOutputPort())
mapBookshelf2Bottom.ScalarVisibilityOff()
bookshelf2BottomActor = vtkActor()
bookshelf2BottomActor.SetMapper(mapBookshelf2Bottom)
bookshelf2BottomActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2Front = vtkStructuredGridGeometryFilter()
bookshelf2Front.SetInputConnection(reader.GetOutputPort())
bookshelf2Front.SetExtent(13, 20, 15, 15, 0, 11)
mapBookshelf2Front = vtkPolyDataMapper()
mapBookshelf2Front.SetInputConnection(bookshelf2Front.GetOutputPort())
mapBookshelf2Front.ScalarVisibilityOff()
bookshelf2FrontActor = vtkActor()
bookshelf2FrontActor.SetMapper(mapBookshelf2Front)
bookshelf2FrontActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2Back = vtkStructuredGridGeometryFilter()
bookshelf2Back.SetInputConnection(reader.GetOutputPort())
bookshelf2Back.SetExtent(13, 20, 19, 19, 0, 11)
mapBookshelf2Back = vtkPolyDataMapper()
mapBookshelf2Back.SetInputConnection(bookshelf2Back.GetOutputPort())
mapBookshelf2Back.ScalarVisibilityOff()
bookshelf2BackActor = vtkActor()
bookshelf2BackActor.SetMapper(mapBookshelf2Back)
bookshelf2BackActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2LHS = vtkStructuredGridGeometryFilter()
bookshelf2LHS.SetInputConnection(reader.GetOutputPort())
bookshelf2LHS.SetExtent(13, 20, 15, 19, 0, 0)
mapBookshelf2LHS = vtkPolyDataMapper()
mapBookshelf2LHS.SetInputConnection(bookshelf2LHS.GetOutputPort())
mapBookshelf2LHS.ScalarVisibilityOff()
bookshelf2LHSActor = vtkActor()
bookshelf2LHSActor.SetMapper(mapBookshelf2LHS)
bookshelf2LHSActor.GetProperty().SetColor(.8, .8, .6)

bookshelf2RHS = vtkStructuredGridGeometryFilter()
bookshelf2RHS.SetInputConnection(reader.GetOutputPort())
bookshelf2RHS.SetExtent(13, 20, 15, 19, 11, 11)
mapBookshelf2RHS = vtkPolyDataMapper()
mapBookshelf2RHS.SetInputConnection(bookshelf2RHS.GetOutputPort())
mapBookshelf2RHS.ScalarVisibilityOff()
bookshelf2RHSActor = vtkActor()
bookshelf2RHSActor.SetMapper(mapBookshelf2RHS)
bookshelf2RHSActor.GetProperty().SetColor(.8, .8, .6)

window = vtkStructuredGridGeometryFilter()
window.SetInputConnection(reader.GetOutputPort())
window.SetExtent(20, 20, 6, 13, 10, 13)
mapWindow = vtkPolyDataMapper()
mapWindow.SetInputConnection(window.GetOutputPort())
mapWindow.ScalarVisibilityOff()
windowActor = vtkActor()
windowActor.SetMapper(mapWindow)
windowActor.GetProperty().SetColor(.3, .3, .5)

outlet = vtkStructuredGridGeometryFilter()
outlet.SetInputConnection(reader.GetOutputPort())
outlet.SetExtent(0, 0, 9, 10, 14, 16)
mapOutlet = vtkPolyDataMapper()
mapOutlet.SetInputConnection(outlet.GetOutputPort())
mapOutlet.ScalarVisibilityOff()
outletActor = vtkActor()
outletActor.SetMapper(mapOutlet)
outletActor.GetProperty().SetColor(0, 0, 0)

inlet = vtkStructuredGridGeometryFilter()
inlet.SetInputConnection(reader.GetOutputPort())
inlet.SetExtent(0, 0, 9, 10, 0, 6)
mapInlet = vtkPolyDataMapper()
mapInlet.SetInputConnection(inlet.GetOutputPort())
mapInlet.ScalarVisibilityOff()
inletActor = vtkActor()
inletActor.SetMapper(mapInlet)
inletActor.GetProperty().SetColor(0, 0, 0)

outline = vtkStructuredGridOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())
mapOutline = vtkPolyDataMapper()
mapOutline.SetInputConnection(outline.GetOutputPort())
outlineActor = vtkActor()
outlineActor.SetMapper(mapOutline)
outlineActor.GetProperty().SetColor(0, 0, 0)

# Now create the usual graphics stuff.
ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


ren.AddActor(table1Actor)
ren.AddActor(table2Actor)
ren.AddActor(FilingCabinet1Actor)
ren.AddActor(FilingCabinet2Actor)
ren.AddActor(bookshelf1TopActor)
ren.AddActor(bookshelf1BottomActor)
ren.AddActor(bookshelf1FrontActor)
ren.AddActor(bookshelf1BackActor)
ren.AddActor(bookshelf1LHSActor)
ren.AddActor(bookshelf1RHSActor)
ren.AddActor(bookshelf2TopActor)
ren.AddActor(bookshelf2BottomActor)
ren.AddActor(bookshelf2FrontActor)
ren.AddActor(bookshelf2BackActor)
ren.AddActor(bookshelf2LHSActor)
ren.AddActor(bookshelf2RHSActor)
ren.AddActor(windowActor)
ren.AddActor(outletActor)
ren.AddActor(inletActor)
ren.AddActor(outlineActor)
ren.AddActor(streamTubeActor)
ren.AddActor(glyphActor)

ren.SetBackground(slate_grey)

# Here we specify a particular view.
aCamera = vtkCamera()
aCamera.SetClippingRange(0.726079, 36.3039)
aCamera.SetFocalPoint(2.43584, 2.15046, 1.11104)
aCamera.SetPosition(-4.76183, -10.4426, 3.17203)
aCamera.SetViewUp(0.0511273, 0.132773, 0.989827)
aCamera.SetViewAngle(15.604)
aCamera.Zoom(1.2)

ren.SetActiveCamera(aCamera)
renWin.SetSize(800, 400)

iren.Initialize()
renWin.Render()
iren.Start()

