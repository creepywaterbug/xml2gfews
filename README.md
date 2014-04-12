### xml2GFEWS
[groovyFEWS](www.github.com/flowmatters/groovyfews) is made by [flowmatters](www.github.com/flowmatters) to offer a better / easier way to maintain the configuration files of [Delft-FEWS](http://www.deltares.nl/en/software/479962/delft-fews). groovyFEWS is using Helper files to do this. The problem is when you have an existing FEWS (xml) configuration you first need to convert this to groovyFEWS code. The uncompile functin of groovyFEWS is not aware of Helper files and cannot smartly construct the groovyFEWS code.

xml2GFEWS is a python script which is converting FEWS (xml) configuration into groovyFEWS code in which it both creates the needed helper file and the regular groovy code which is pointing to the helper files. Well this is probably a bit overstated. At this moment xml2GFEWS is only able to create one kind of Helper yet. This helper is organizing default values out of the elements under the 'timeSeriesSet' and 'timeSeriesSets' tags.

### Operation
You need to install python and sqlite on your system. You also need the python libraries python-pysqlite2 and python-lxml. Put the xml configuration file you want to be converted in the same working directory as you put xml2GEWS.py. Edit xml2GEWS.py to change the names of the in- and output files. 

<code>python xml2GFEWS.py<code>

This will create a regular groovy file and a helper groovy file. I hope the example code underneath is clear enough to illustrates what is actually happening.

**Input: FEWS xml**
~~~xml
<?xml version="1.0" encoding="UTF-8"?>
<filters version="1.1">
	<defaultFilterId>DADIDA</defaultFilterId>
	<timeSeriesSets id="Set1">
		<timeSeriesSet>
			<moduleInstanceId>ImportA</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parA</parameterId>
			<locationSetId>TRE_waterstand</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep multiplier="3" unit="minute"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>read only</readWriteMode>
			<synchLevel>1</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportA</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parB</parameterId>
			<locationSetId>TRE_niveau</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep multiplier="3" unit="minute"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>read only</readWriteMode>
			<synchLevel>1</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportA</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parB.dag</parameterId>
			<locationSetId>TRE_niveau_dag</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>read only</readWriteMode>
			<synchLevel>1</synchLevel>
		</timeSeriesSet>
	</timeSeriesSets>		
	<timeSeriesSets id="Set2">
		<timeSeriesSet>
			<moduleInstanceId>ImportB</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parA</parameterId>
			<locationSetId>TRE_waterstand</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep multiplier="3" unit="minute"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportB</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parB</parameterId>
			<locationSetId>TRE_niveau</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep multiplier="3" unit="minute"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportB</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parB.dag</parameterId>
			<locationSetId>TRE_niveau_dag</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-14" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
	</timeSeriesSets>
	<filter id="ABCD" name="EFGHI">
		<timeSeriesSet>
			<moduleInstanceId>ImportD</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parC</parameterId>
			<locationSetId>locC</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-30" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportD</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parD</parameterId>
			<locationSetId>locD</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-30" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportC</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parE</parameterId>
			<locationSetId>locE</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-30" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportD</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parF</parameterId>
			<locationSetId>locF</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-60" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
		<timeSeriesSet>
			<moduleInstanceId>ImportD</moduleInstanceId>
			<valueType>scalar</valueType>
			<parameterId>parG</parameterId>
			<locationSetId>locG</locationSetId>
			<timeSeriesType>external historical</timeSeriesType>
			<timeStep unit="nonequidistant"/>
			<relativeViewPeriod end="0" start="-30" unit="day"/>
			<readWriteMode>editing visible to all future task runs</readWriteMode>
			<synchLevel>5</synchLevel>
		</timeSeriesSet>
	</filter>
</filters>
~~~
**Output: Helper groovy file**
~~~groovy
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
~~~
**Output: Regular groovy file**
~~~groovy
import static GroovyFewsHelpers.*
import groovy.xml.StreamingMarkupBuilder
import groovy.xml.XmlUtil
def outputFile = new File(args[0])
def writer = outputFile.newWriter()
def xmlBuilder = new StreamingMarkupBuilder()
xmlBuilder.useDoubleQuotes=true
def builderResult = xmlBuilder.bind {
filters('version': '1.1') {
	defaultFilterId('DADIDA')
	timeSeriesSets(id:'Set1') {
		__Helpers.tss_Set1(
			parameterId:'parA',
			locationSetId:'TRE_waterstand',
			delegate
		)
		__Helpers.tss_Set1(
			parameterId:'parB',
			locationSetId:'TRE_niveau',
			delegate
		)
		__Helpers.tss_Set1(
			parameterId:'parB.dag',
			locationSetId:'TRE_niveau_dag',
			timeStep:['unit': 'nonequidistant'],
			delegate
		)
	}
	timeSeriesSets(id:'Set2') {
		__Helpers.tss_Set2(
			parameterId:'parA',
			locationSetId:'TRE_waterstand',
			delegate
		)
		__Helpers.tss_Set2(
			parameterId:'parB',
			locationSetId:'TRE_niveau',
			delegate
		)
		__Helpers.tss_Set2(
			parameterId:'parB.dag',
			locationSetId:'TRE_niveau_dag',
			timeStep:['unit': 'nonequidistant'],
			delegate
		)
	}
	filter('id': 'ABCD', 'name': 'EFGHI') {
		__Helpers.tss_None(
			parameterId:'parC',
			locationSetId:'locC',
			delegate
		)
		__Helpers.tss_None(
			parameterId:'parD',
			locationSetId:'locD',
			delegate
		)
		__Helpers.tss_None(
			moduleInstanceId:'ImportC',
			parameterId:'parE',
			locationSetId:'locE',
			delegate
		)
		__Helpers.tss_None(
			parameterId:'parF',
			locationSetId:'locF',
			relativeViewPeriod:['start': '-60', 'end': '0', 'unit': 'day'],
			delegate
		)
		__Helpers.tss_None(
			parameterId:'parG',
			locationSetId:'locG',
			delegate
		)
	}
}
}
writer << XmlUtil.serialize(builderResult)
writer.close()
~~~
