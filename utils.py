import yaml
import log
import  psycopg2, json
import dateutil.parser as dp
creds = yaml.safe_load(open('./config/config_postgres.yaml'))
conf = yaml.safe_load(open('./config/config_catchpoint.yaml'))
logger = log.get_logger(__name__,conf['log_file'],conf['log_level'])


class Utils():
    @staticmethod
    def parse_raw(structure):
        logger.info("Parsing JSon")
        synthetic_metrics = []
        if 'error' in structure:
            logger.error(structure['error'])
        if 'detail' not in structure:
            logger.error('No data available')
            return None    
        test_params = []
        final_list = [] #list of all jsons
        synthetic_metrics = structure['detail']['fields']['synthetic_metrics']
        
        for i in synthetic_metrics:
            metrics = i['name']
            test_params.append(metrics)
        
        for value in structure['detail']['items']:
            values = {} # json which contains tags fields time 
            
            
            values['breakdown_1'] = value['breakdown_1']['name']
            values['breakdown_2'] = value['breakdown_2']['name']
            if 'step' in value:
                values['step'] = value['step']
            if 'hop_number' in value:
                values['hop_number'] = value['hop_number']
        
            
            values['time_stamp'] = dp.parse(value['dimension']['name']).timestamp()*1000000

            metric_values = value['synthetic_metrics']
            fields = {}
            for i in range(0,len(metric_values),1):
                fields[test_params[i]]=metric_values[i]
            values['metrics'] = fields
            final_list.append(values)
        return final_list
                

    @staticmethod
    def write_data(data):
        logger.info("Pushing data to PostgreSQL")
        try:
            with psycopg2.connect('dbname={0} user={1} password={2}'.format(creds['dbname'],creds['user'],creds['pw'])) as conn:
                with conn.cursor() as cur:
                    cur.execute(""" create table if not exists {0}(id serial NOT NULL PRIMARY KEY, info json NOT NULL) """.format(creds['table_name']))
                    for i in data: 
                        cur.execute("""INSERT INTO {0}(info)VALUES( '{1}' )""".format(creds['table_name'],json.dumps(i)))
            
        except Exception as e:
            logger.exception(str(e))
            logger.exception('Error while writing data')


    @staticmethod
    def validate_configurations():
        if 'client_id' not in conf or conf['client_id'] is None:
            return False
        if 'client_secret' not in conf or conf['client_secret'] is None:
            return False
        if 'protocol' not in conf or conf['protocol'] is None: 
            return False
        if 'domain' not in conf or conf['domain'] is None:
            return False 
        if 'token_endpoint' not in conf or conf['token_endpoint'] is None: 
            return False
        if 'rawdata_endpoint' not in conf or conf['rawdata_endpoint'] is None:
            return False
        return True