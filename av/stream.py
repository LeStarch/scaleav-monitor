import gi
import time
gi.require_version("Gst","1.0")
from gi.repository import  Gst, GstVideo

class BaseStream(object):
    '''
    @author starchmd
    Base GStreamer stream
    '''
    running=None
    def __init__(self,name,stages):
        '''
        Initializes this pipeline
        @param name - name of the pipeline
        @param stages - ordered list of gst elements names in the pipeline
        '''
        self.build(name,stages)
    def build(self,name,stages):
        '''
        Build the GStreamer pipeline
        @param name - name of the pipeline
        @param stages - ordered list of gst elements names in the pipeline
        '''
        self.pipeline = Gst.Pipeline(name)
        #Basic bus setup
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message::error",self.onError)
        #TODO: Handel EOS (message::eos)
        self.bus.enable_sync_message_emission()
        self.bus.connect("sync-message::element",self.onSync)
        #Build the stages 
        for index in range(0,len(stages)):
            elem = Gst.ElementFactory.make(stages[index],str(index))
            self.pipeline.add(elem)
            if index > 0:
                self.pipeline.get_child_by_name(str(index-1)).link(elem)
        self.running = False
    def onSync(self,bus,msg):
        '''
        What to do on sync requests
        @param bus - bus relaying message
        @param msg - message sent
        '''
        pass
    def onError(self,bus,msg):
        '''
        What to do on errors
        @param bus - bus relaying message
        @param msg - message sent
        '''
        print("Error:",msg.parse_error())
    def start(self):
        '''
        Runs the stream
        '''
        if self.running is None:
            raise StreamNotBuiltException()
        self.running = True
        self.pipeline.set_state(Gst.State.PLAYING)
    def stop(self):
        '''
        Stop the stream
        '''
        if self.running is None:
            raise StreamNotBuiltException()
        self.pipeline.set_state(Gst.State.NULL)
        self.running = False
class StreamNotBuiltException(Exception):
    '''
    @author starchmd
    An exception thrown when the stream is not built but other functions are called
    '''
    pass
