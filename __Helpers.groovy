static def tss_default(Map map,d) {
	def defaults= [
		'synchLevel':'5'
		,'locationSetId':'NonDefault'
		,'timeStep':['unit': 'nonequidistant']
		,'valueType':'scalar'
		,'parameterId':'NonDefault'
		,'relativeViewPeriod':['start': '-14', 'end': '0', 'unit': 'day']
		,'readWriteMode':'editing visible to all future task runs'
		,'moduleInstanceId':'NonDefault'
		,'timeSeriesType':'external historical'
	]
	def params = defaults + map
	d.timeSeriesSet() { ['synchLevel','locationSetId','timeStep','valueType','parameterId','relativeViewPeriod','readWriteMode','moduleInstanceId','timeSeriesType'].each { k ->
		"$k"(params[k])
		}
	}
}

static def tss_Set1(Map map,d) {
	def Set1_params = [
		'synchLevel':'1'
		,'timeStep':['unit': 'minute', 'multiplier': '3']
		,'readWriteMode':'read only'
		,'moduleInstanceId':'ImportA'
	]
	tss_default(Set1_params + map,d)
}

static def tss_Set2(Map map,d) {
	def Set2_params = [
		'timeStep':['unit': 'minute', 'multiplier': '3']
		,'moduleInstanceId':'ImportB'
	]
	tss_default(Set2_params + map,d)
}

static def tss_None(Map map,d) {
	def None_params = [
		'relativeViewPeriod':['start': '-30', 'end': '0', 'unit': 'day']
		,'moduleInstanceId':'ImportD'
	]
	tss_default(None_params + map,d)
}

