import pyxid2 as pyxid, time
from psychopy import core

pyxid.use_response_pad_timer = True

device = pyxid.get_xid_devices()[0]

time.sleep(1)

device.reset_base_timer() #should be called just before first trial


for i in range(10):
    if device.is_response_device():
        
        # This should poll and clear all responses from the box before the actual response is expected
    #        numb = 0
        device.poll_for_response()
        while device.has_response():
            device.clear_response_queue()
            device.poll_for_response()
    #            numb += 1

    #            print('number %s, cleared response %s'%(numb, re))

    #        print('device has no more responses')


        clock_loc = core.Clock()
        release = False
        clock_loc.reset(10)
        device.reset_rt_timer()

        # Set everything to None in case I have a weird answer
        Press_key = None
        ReleaseResponse_loc = None
        Time_key = None

        while not release:

            if clock_loc.getTime() >= 0:
                Press_key = None
                ReleaseResponse_loc = None
                Time_key = None
                break

            device.poll_for_response()

            if device.has_response():
                resp = device.get_next_response()


                if resp['pressed']: 
                    Press_key = resp['key']
                    Time_key = resp['time']
                    ReleaseResponse_loc = None
                    print('Pressed:\n', Press_key,Time_key, sep='    ')

                elif not resp['pressed']:
                    ReleaseResponse_loc = resp
                    release = True
                    print('\n\nRelased:\n', ReleaseResponse_loc, sep='    ')
                    if Press_key is None:
                        print('Button was pressed before polling!')


                else:
                    print('Something is wrong with this response %s'%resp)
                    ReleaseResponse_loc = None
                    Press_key = None
                    Time_key = None

    else:
        print('device %s is not a response device!'%device)
        ReleaseResponse_loc = None
        Press_key = None
        Time_key = None
    print('sleeping...\n\n')
    time.sleep(5)

#cycle = 0
#clock = core.Clock()
#
#for i in range(10):
#    cycle += 1
#    clock.reset(5)
#    device.reset_base_timer()
#    device.clear_response_queue()
#    device.reset_rt_timer()
#    release = True
#
#    if device.is_response_device():
#
#        while release:
#    
#
#            device.poll_for_response()
#
#            if device.has_response():
#                resp = device.get_next_response()
#
#                if resp['pressed']:
#                    PressResponse = resp
#                    t1 = clock.getTime()
#
#                else:
#                    ReleaseResponse = resp
#                    release = False
#                    t2 = clock.getTime()
#
#
#
#        print('---------------------------------------------------------------------------------\nCycle %s:'%cycle, resp, sep = '\n')
#        #PressResponse,'PressResponse timing %s at clock %s,ReleaseResponse timing %s at clock %s'%(PressResponse['time'], (t1 + 5) * 1000, ReleaseResponse['time'],(t2 + 5) * 1000))
#        
#        print(device.has_response(), device.response_queue)
#        
#        for i in range(7):
#            if PressResponse['key'] == i:
#                print('{} key press'.format(i))
#        
#    else:
#            print('device %s is not a response device!'%device)
#    times = 4
#    print('sleeping for %s\n\n----------------------------------------------------------------------------------'%times)
#    time.sleep(times)
#    
#    #I think that one problem is that on the second response polling the button release gets registered somehow. Before each response I should clear rt timer, clear queue events and wait for polling.
#    
#    response2 = device.get_next_response()
#    print('Response2 is %s and queue size is %s'%(response2, device.response_queue_size()))
#
#    device.clear_response_queue()
#
#    while not device.has_response():
#         device.poll_for_response()
#
#        ## register the received response
#    response3 = device.get_next_response()
#        
#    print('Response3 is %s and queue size is %s'%(response3, device.response_queue_size()))
#
#
#for i in range(0):
#    numb = 0
#    while True:
#        device.poll_for_response()
#        if device.has_response():
#            re = device.get_next_response()
#            numb += 1
#            print('number %s, cleared response %s'%(numb, re))
#            device.clear_response_queue()
#        else:
#            print('device has no more response')
#            break
#    print('sleeping for 8')
#    time.sleep(8)
#
#
#for i in range(0):
#        numb = 0
#        device.poll_for_response()
#        while device.has_response():
#            numb += 1
#            re = device.get_next_response()
#            print('number %s, cleared response %s'%(numb, re))
#            device.poll_for_response()
#        print('device has no more responses')
#        print('sleeping for 8')
#        time.sleep(8)
#
