import json
from threading import Thread


# Save Products to Json file
class JsonSaveProducts:
    
    # Constructor function
    def __init__(self, filename):
        # Helper
        self.filename = filename
        self.stopped = False
        self.products_buffer = list()

    # Main handler function for the multi threading
    def start(self):
        print("[*] Starting Json Save Thread")
        Thread(target=self.update, args=()).start()
        return self
    
    # Runs on Multi Thread
    def update(self):
        # Save product into a json file
        with open(self.filename, 'w') as outfile:
            # Keep Running for Thread Life
            while True:
                # keep looping infinitely until the thread is stopped
                if len(self.products_buffer) > 0:
                    try:
                        # Save oldest product
                        json.dump(self.products_buffer[0], outfile, indent=0)
                        # Remove oldest product
                        self.products_buffer.pop(0)
                        print("[**] Successfully Uploaded Product")
                        print("[*] Buffer Size: {}".format(len(self.products_buffer)))
                    except:
                        # Failed to save product into db.
                        # TODO: Add err message
                        print("[-] Upload Error")
                        self.stopped = True

                # if the thread indicator variable is set, stop the thread
                # and resource camera resources
                if self.stopped:
                    outfile.close()
                    return
                    
    def append(self, product):
        # Append product into buffer
        result = False
        if product is not None:
            self.products_buffer.append(product)
            result = True
        return result
            
    def alive(self):
        if len(self.products_buffer) < 1: 
            return False
        else:
            return True
        
    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
