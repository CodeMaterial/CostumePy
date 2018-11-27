def launch_costume(launch_file):

    '''
    TODO
    Launches the entire costume from a .launch file

    :param launch_file:
    :return costume manager:

    '''
    pass


def test(node_name):

    '''
    TODO
    Creates a test object for a set node
    Could be used with multiple node names to both unit and end-to-end test?

    :param node_name: Identifier of the node to test
    :return:
    '''
    pass


def limit(framerate):

    '''
    TODO
    Limits the framerate of the mainloop

    :param framerate:
    :return:
    '''
    pass


def is_running():

    '''
    TODO
    Checks to see if node hasn't been stopped by an external command.
    Used in mainloops and testing.

    :return if node is running:
    '''
    pass


def broadcast(message_jd, data=None):

    '''
    TODO
    Broadcasts a message with message_id and data if needed

    :param message:
    :param data:
    :return success:
    '''
    pass


def listen(message_id, callback, args=None):

    '''
    TODO
    Listens for a particular message id and passes it on to the callback with attached args

    :param message_id:
    :param callback:
    :param args:
    :return:
    '''
    pass


def set_name(node_name):

    '''
    TODO
    Sets the id / name of the node.
    By default this should be the relative path I think or filename

    :param node_name:
    :return:
    '''
    pass


def message(message_id, data=None):

    '''
    TODO
    Returns a message object just for ease of use

    :param message_id:
    :param data:
    :return:
    '''
    pass
