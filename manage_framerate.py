def manage_framerate(delta_frame, fps, space=None):
    if delta_frame < .25:
        """
        This if-statement prevents giant steps and tickrates. When the window is moved, processing stops until it is
        released. 0.25 seconds should be a good balance, as I assume that there will never be a normal frame that takes
        longer to calculate than that.
        """
        if space is not None:
            space.tickrate = delta_frame
        fps = int(1 / delta_frame)
    return fps
