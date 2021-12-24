
from weaver import Weaver
from fabric import  task

@task
def deploy(ctx, config):
    weaver = Weaver(config,ctx)
    weaver.run()



      
            




        

