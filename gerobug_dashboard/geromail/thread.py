import threading, logging, time, traceback
from logging.handlers import TimedRotatingFileHandler
from . import geroparser


class RunGeromailThread(threading.Thread):

    def __init__(self, total):
        self.total = total
        threading.Thread.__init__(self)
    
    def run(self):
        restart_count = 0
        thread_id = threading.get_ident()
        
        logging.getLogger("Gerologger").info(f"[THREAD-{thread_id}] Geroparser thread started")
        
        while True:
            try:
                logging.getLogger("Gerologger").info(f"[THREAD-{thread_id}] Starting geroparser.run() [Restart: {restart_count}]")
                geroparser.run()
                logging.getLogger("Gerologger").warning(f"[THREAD-{thread_id}] geroparser.run() returned normally (unexpected)")
                
            except KeyboardInterrupt:
                logging.getLogger("Gerologger").warning(f"[THREAD-{thread_id}] KeyboardInterrupt - stopping gracefully")
                break
                
            except SystemExit as e:
                logging.getLogger("Gerologger").warning(f"[THREAD-{thread_id}] SystemExit({e}) - stopping gracefully")
                break
                
            except BaseException as e:
                restart_count += 1
                logging.getLogger("Gerologger").error(
                    f"[THREAD-{thread_id}] Geroparser Failed [Restart: {restart_count}]: "
                    f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
                )
            
            logging.getLogger("Gerologger").info(f"[THREAD-{thread_id}] Restarting in 30 seconds...")
            time.sleep(30)
        
        logging.getLogger("Gerologger").error(f"[THREAD-{thread_id}] Thread loop stopped - exiting")
