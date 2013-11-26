#!/usr/bin/env python
from rpy2.robjects.packages import importr
import rpy2.robjects as robjects
import logging
import time
grdevices = importr('grDevices')
graphics = importr('graphics')
log = logging.getLogger(__name__)
class Rgraph(object):
    def __init__(self,predictiondb,disdb):
        self.predictiondb = predictiondb
        self.disdb = disdb
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        self.directory = 'output/'
        self.graph_xy_scatter(self.predictiondb)
        self.graph_histogram(self.disdb)
        
    def graph_xy_scatter(self,predictiondb):
        log.info('starting xy scatter plot')
        filename = self.directory + 'xy-scatter-' + self.timestr + '.pdf'
        r = robjects.r
        x = robjects.FloatVector(predictiondb.get_perfect_prediction())
        y = robjects.FloatVector(predictiondb.get_my_prediction())
        grdevices.pdf(file=filename)
        robjects.globalenv["x"] = x
        robjects.globalenv["y"] = y
        r.plot(x,y,xlab="True Prediction",ylab="My Prediction",pch=8,col="blue")
        # graphics.abline(r.lm("y ~ x"))
        r.abline(r.lm("y~x"),col="red")
        correlation = r.cor(x,y)
        slope = r.lm("y~x")[0][1]
        r.text(0.05,0.12,r.paste("r=",r.round(correlation,4)))
        r.text(0.05,0.10,r.paste("m=",r.round(slope,4)))
        log.info('correlation %s',str(correlation))
        log.info('slope %s',str(slope))
        grdevices.dev_off()
    def graph_histogram(self,distancedb):
        log.info('starting histogram plot')
        filename = self.directory + 'histogram-' + self.timestr + '.pdf'
        r = robjects.r
        x = robjects.FloatVector(distancedb.get_distances())
        grdevices.pdf(file=filename)
        mybins = robjects.FloatVector([0.0,0.25,0.5,0.75,1.0])
        r.hist(x,breaks=mybins)
        # r.hist(x,col="lightgreen",main="Histogram",breaks=mybins)
        # r.hist(distancedb.get_distances(),col="lightgreen",main="Histogram",breaks=mybins)
        grdevices.dev_off()
def main():
    print 'hello'
    x = ['0.0208333333333','0.0208333333333','0.0208333333333','0.0416666666667','0.0208333333333']
    y = ['0.0263157894737','0.0263157894737','0.0263157894737','0.0526315789474','0.0263157894737']
    # xyscatter = Rgraph()
    # xyscatter.graph_xy_scatter(x,y)

if __name__ == '__main__':
    main()
        