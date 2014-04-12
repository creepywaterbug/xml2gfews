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
