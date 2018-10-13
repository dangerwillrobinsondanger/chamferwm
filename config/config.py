
import chamfer
from enum import Enum,auto

class Key(Enum):
	FOCUS_RIGHT = auto()
	FOCUS_LEFT = auto()
	FOCUS_UP = auto()
	FOCUS_DOWN = auto()
	FOCUS_PARENT = auto()
	FOCUS_CHILD = auto()

	LAYOUT = auto()
	SPLIT_V = auto()

class Container(chamfer.ContainerA):
	def OnSetup(self): #later on this will take parameters
		print("OnSetup");
		self.minSize = (0.4,0.2);
		self.test = 23.0;
		print(self.minSize);
		
class Backend(chamfer.Backend):
	def OnSetupKeys(self, binder):
		print("setting up keys...");

		binder.BindKey(ord('l'),chamfer.MOD_MASK_1,Key.FOCUS_RIGHT.value);
		binder.BindKey(ord('h'),chamfer.MOD_MASK_1,Key.FOCUS_LEFT.value);
		binder.BindKey(ord('k'),chamfer.MOD_MASK_1,Key.FOCUS_UP.value);
		binder.BindKey(ord('j'),chamfer.MOD_MASK_1,Key.FOCUS_DOWN.value);
		binder.BindKey(ord('a'),chamfer.MOD_MASK_1,Key.FOCUS_PARENT.value);
		binder.BindKey(ord('x'),chamfer.MOD_MASK_1,Key.FOCUS_CHILD.value);

		binder.BindKey(ord('e'),chamfer.MOD_MASK_1,Key.LAYOUT.value);
		#bunder.BindKey(chamfer.KEY_TAB,chamfer.MOD_MASK_1,Key.SPLIT_V.value);

		#/ - search for a window
		#n - next match
		#N - previous match

		#debug only
		binder.BindKey(ord('h'),chamfer.MOD_MASK_SHIFT,Key.FOCUS_LEFT.value);
		binder.BindKey(ord('k'),chamfer.MOD_MASK_SHIFT,Key.FOCUS_UP.value);
		binder.BindKey(ord('l'),chamfer.MOD_MASK_SHIFT,Key.FOCUS_RIGHT.value);
		binder.BindKey(ord('j'),chamfer.MOD_MASK_SHIFT,Key.FOCUS_DOWN.value);

		binder.BindKey(ord('e'),chamfer.MOD_MASK_SHIFT,Key.LAYOUT.value);
	
	#def OnSetupClient(self, client):
		#client.borderWidth = (0.02,0.02);
		#print(client.minSize);
		#client.minSize = (0.4,0.2); #note: doesn't work. client is a copy object
		#print(client.minSize);
		#print(client.minSize);

		#return the container under which to create this new one
		#focus = chamfer.GetFocus();
		#parent = focus.GetParent();
		#if parent is None:
		#	return focus;
		#return parent;
		#TODO: self.borderWidth?

		#client.SetBorderWidth(0.02,0.02);
		#client.SetParent(parent);
		#pass
	
	def OnCreateContainer(self):
		print("OnCreateContainer()");
		return Container();

	def OnCreateClient(self, client):
		container = client.GetContainer();
		chamfer.SetFocus(container);

	def OnKeyPress(self, keyId):
		print("key press: {}".format(keyId));
		focus = chamfer.GetFocus();
		parent = focus.GetParent();
		if parent is None:
			return; #root container

		if keyId == Key.FOCUS_RIGHT.value and parent.layout == chamfer.layout.VSPLIT:
			#should GetNext() jump to the next container in parent if this is the last in this level?
			#maybe additional GetNext2() for that
			focus = focus.GetNext();
			chamfer.SetFocus(focus);

		elif keyId == Key.FOCUS_LEFT.value and parent.layout == chamfer.layout.VSPLIT:
			focus = focus.GetPrev();
			chamfer.SetFocus(focus);

		elif keyId == Key.FOCUS_DOWN.value and parent.layout == chamfer.layout.HSPLIT:
			focus = focus.GetNext();
			chamfer.SetFocus(focus);

		elif keyId == Key.FOCUS_UP.value and parent.layout == chamfer.layout.HSPLIT:
			focus = focus.GetPrev();
			chamfer.SetFocus(focus);
			
		elif keyId == Key.LAYOUT.value:
			layout = {
				chamfer.layout.VSPLIT:chamfer.layout.HSPLIT,
				chamfer.layout.HSPLIT:chamfer.layout.VSPLIT
			}[parent.layout];
			parent.ShiftLayout(layout); #TODO: layout = ..., use UpdateLayout() to update all changes?
		
		elif keyId == Key.SPLIT_V.value:
			#arm the container split
			pass;
	
	def OnKeyRelease(self, keyId):
		print("key release: {}".format(keyId));

class Compositor(chamfer.Compositor):
	def __init__(self):
		#self.shaderPath = "../";
		print(self.shaderPath);
	
	#def SetupGraphics(self):
	#	shader = self.LoadShader("frame_vertex.spv");

	def OnPropertyChange(self, prop):
		pass;

backend = Backend();
chamfer.bind_Backend(backend);

#compositor = Compositor();
#chamfer.bind_Compositor(compositor);

#startup applications here?
