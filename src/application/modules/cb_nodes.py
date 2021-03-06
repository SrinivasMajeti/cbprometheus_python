from cb_utilities import *

def _get_metrics(user, passwrd, node_list, cluster_name, result_set=60):
    '''gets the metrics for each node'''
    result = {}
    result['metrics'] = []
    auth = basic_authorization(user, passwrd)
    sample_list = get_sample_list(result_set)

    for url in node_list:

        try:
            _url = "http://{}:8091/pools/default".format(url.split(":")[0])
            stats = rest_request(auth, _url)
        except Exception as e:
            print(e)
            return(result)

        convrt_url = url
        for _record in stats:
            record = value_to_string(_record)
            if record == "nodes":
                for node in stats[record]:
                    try:
                        if 'thisNode' in node.keys():
                            for _metric in node:
                                metric = value_to_string(_metric)
                                if metric in ["thisNode"]:
                                    pass
                                else:
                                    if metric in [
                                        "nodeEncryption", "clusterMembership", "recoveryType", "status"]:
                                        if metric == "clusterMembership":
                                            if node[metric] == "active":
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 1))
                                            else:
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 0))
                                        if metric == "nodeEncryption":
                                            if node[metric] == "True":
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 1))
                                            else:
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 0))
                                        if metric == "recoveryType":
                                            if node[metric] == "none":
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 0))
                                            else:
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 1))
                                        if metric == "status":
                                            if node[metric] == "healthy":
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 1))
                                            else:
                                                result['metrics'].append(
                                                    "{} {{cluster=\"{}\", node=\"{}\", "
                                                    "type=\"node\"}} {}".format(
                                                        snake_caseify(metric), cluster_name, convrt_url, 0))
                                    elif metric in ["ports",
                                                    "services",
                                                    "couchApiBase",
                                                    "couchApiBaseHTTPS",
                                                    "version",
                                                    "os",
                                                    "hostname",
                                                    "otpNode",
                                                    "memoryFree", # this is a duplicate from systemStats.mem_free
                                                    "memoryTotal",  # this is a duplicate from systemStats.mem_total
                                                    "configuredHostname",
                                                    "externalListeners",
                                                    "addressFamily",
                                                    "nodeUUID"
                                                    ]:
                                        pass
                                    elif metric == "interestingStats":
                                        for _metric in node[metric]:
                                            result['metrics'].append(
                                                "{} {{cluster=\"{}\", node=\"{}\", "
                                                "type=\"node\"}} {}".format(
                                                    snake_caseify(_metric),
                                                    cluster_name,
                                                    convrt_url,
                                                    node[metric][_metric]))
                                    elif metric == "systemStats":
                                        for _metric in node[metric]:
                                            result['metrics'].append(
                                                "{} {{cluster=\"{}\", node=\"{}\", "
                                                "type=\"node\"}} {}".format(
                                                    snake_caseify(_metric),
                                                    cluster_name,
                                                    convrt_url,
                                                    node[metric][_metric]))
                                    else:
                                        result['metrics'].append(
                                            "{} {{cluster=\"{}\", node=\"{}\", "
                                            "type=\"node\"}} {}".format(
                                                snake_caseify(metric),
                                                cluster_name,
                                                convrt_url,
                                                node[metric]))
                    except Exception as e:
                        print("buckets: " + str(e))

    return(result)
