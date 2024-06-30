from closeTesterScheduled import closeTester
from sendEmail	import sendEmail

closedTicks = closeTester()
sendEmail([],closedTicks)