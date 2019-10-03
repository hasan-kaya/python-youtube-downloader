from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from redis import Redis
from rq.job import Job
from rq import Queue
from utils import get_download_links
import sys

redis_conn = Redis()
queue = Queue(connection=redis_conn)

PORT_NUMBER = 8080
estimated_time = 2

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        job_id = self.path.replace("/", "")
        if job_id:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                job = Job.fetch(job_id, connection=redis_conn)
                if job.is_finished:
                    ret = job.return_value
                elif job.is_queued:
                    waiting_jobs = queue.get_job_ids()
                    order = waiting_jobs.index(job_id) + 1
                    ret = {'status': 'in-queue', 'time': order * estimated_time}
                elif job.is_started:
                    ret = {'status': 'started', 'time': estimated_time}
                elif job.is_failed:
                    ret = {'status': 'failed'}
                self.wfile.write(ret)
            except:
                job = queue.enqueue_call(func=get_download_links,
                                         args=(job_id,),
                                         result_ttl=-1,
                                         job_id=job_id)
                ret = {'time': (len(queue.jobs) + 1) * estimated_time}
                self.wfile.write(ret)
            return

try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ', PORT_NUMBER)
    server.serve_forever()
except KeyboardInterrupt:
    print
    '^C received, shutting down the web server'
    server.socket.close()
    