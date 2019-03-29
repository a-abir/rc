class Segment:
    def __init__(self, *args, **kwargs):
        self.done = False

    def config(self, robot):
        '''
        this is basically this path's __init__, but you can overload this method :)
        
        it's called when the path starts this segment
        '''
        pass

    def update(self, robot):
        '''
        overload me!

        this is called every time the path is updated
        '''
        pass

    def finish(self):
        '''
        finishes your path segment
        '''
        self.done = True

    def is_done(self):
        '''
        tells you whether or not your path segment is done
        '''
        return self.done 

    def __str__(self): return "<" + type(self).__name__ + " Segment>"


class Path:
    def __init__(self, robot, *segments, **kwargs):
        '''
        Don't overload me!
        '''
        self.config(robot, *segments, **kwargs)
        self.segments = segments
        self.segment_index = 0
        self.done = False

        self.current_segment().config(robot)

    def config(self, robot, *segments, **kwargs):
        '''
        this is basically this path's __init__, but you can overload this method :)
        '''
        pass

    def segment_done(self):
        '''
        tells you whether or not your current path segment is done
        '''
        return self.current_segment().is_done()

    def current_segment(self):
        '''
        gets your path's current segment
        '''
        return self.segments[self.segment_index]

    def next_segment(self):
        '''
        gets your path's next segment
        '''
        return self.segments[self.segment_index + 1]

    def check_segment_change(self, robot):
        '''
        do not use me!
        '''
        if self.segment_done():
            self.segment_index += 1
            if self.segment_index >= len(self.segments):
                self.finish()
            else:
                self.current_segment().config(robot)

    def finish(self):
        '''
        finishes your path
        '''
        self.done = True

    def is_done(self):
        '''
        tells you whether or not your path is done
        '''
        return self.done

    def update(self, robot):
        '''
        update your path
        '''
        self.current_segment().update(robot)

        self.check_segment_change(robot)