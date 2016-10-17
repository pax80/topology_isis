from lxml import objectify, etree
from py2neo import Graph, Relationship, Node

filename = "/home/vagrant/topo_test_topology/ISIS_DB"
neo = "http://neo4j:oBs3rv3r@127.0.0.1:7474/db/data/"
graph = Graph(neo)



MASK = {
    '32': 'loopback',
    '30': 'p2p'
}

def return_list(key, xml):
    list_return = [{n.tag.split("}")[1]: n for n in n_el.getchildren()} for
                   n_el in xml[key]]
    return list_return


def create_dict_from_xml(filename):
    root = objectify.parse(filename).getroot()
    entries = root.findall(".//{*}isis-database-entry")
    db_isis = []
    for entry in entries:
        lsa = {i.tag.split("}")[1]: i for i in entry.getchildren()}
        if 'isis-neighbor' in lsa:
            lsa['isis-neighbor'] = return_list('isis-neighbor', lsa)

        if 'isis-prefix' in lsa:
            lsa['isis-prefix'] = return_list('isis-prefix', lsa)

        # print("{}".format(lsa))

        db_isis.append(lsa)

    return db_isis


def create_node(label, node):
    node_a = Node(label, **node)
    a = graph.create(node_a)
    if len(a) == 1:
        print("node created {}".format(str(a[0])))
        return a[0]

def create_attached_link(re):
    a = graph.create(re)
    if len(a) == 1:
        print("relationship created {}".format(str(a[0])))
        return a[0]

def find_node(key, node):
    query = "MATCH (a) where a.{}='{}' RETURN a".format(key, node[key])
    a = graph.cypher.execute(query)
    return a.one


def create_neig_link(link_type, **kwargs):
    properties = {k: v for (k, v) in kwargs.iteritems() if v is not None}
    query = "MATCH (a:" + self.label + "),(z:" + self.label + ") WHERE a.lsp_id={a_lsp_id} AND z.id={z_lsp_id} "


def search_attach_rel(key_a, node_a, key_b, node_b):
    query = "MATCH (a)-[r]-(b) where a.{}='{}' and b.{}='{}' return r".format(key_a, node_a[key_a], key_b, node_b[key_b])
    r = graph.cypher.execute(query)
    return len(r)




# def create_neig_link(link_type, **kwargs):
#         properties = {k: v for (k, v) in kwargs.iteritems() if v is not None}
#         query = "MATCH (a:" + self.label + "),(z:" + self.label + ") WHERE a.lsp-id={a_lsp_id} AND z.id={z_lsp_id} " \
#                                                                   "CREATE (a)-[r: {properties}]->(z)"
#         .graph_db.cypher.execute(query,
#                                      a_node_id=properties['a_' + self.label + '_id'],
#                                      z_node_id=properties['z_' + self.label + '_id'],
#                                      properties=properties)


def create_topology_from_dict(lsas):
    for lsa in lsas:
        node = {
            'lsp_id': lsa['lsp-id'].text,
            'sequence_number': lsa['sequence-number'].text
        }
        node_q = find_node('lsp_id', node=node)
        if node_q is None:
            node_q = create_node('LSA',node=node)
        if 'isis-prefix' in lsa:
            for px in lsa['isis-prefix']:
                network, mask = px['address-prefix'].text.split('/')
                protocol_type = px['protocol-name'].text
                if mask not in MASK:
                    type = 'lan'
                else:
                    type = MASK[mask]

                prefix = {
                    'network': network,
                    'mask': mask,
                    'protocol_type': protocol_type,
                    'type': type
                }

                prefix_q = find_node('network', prefix)

                if  prefix_q is None:
                    prefix_q = create_node('PREFIX', node=prefix)

                connected = {
                    'prefix_status': px['prefix-status'].text,
                    'metric': int(px['metric'].text),
                    'prefix_flag': px['prefix-flag'].text
                }

                if search_attach_rel('lsp_id',node, 'network', prefix) == 0:
                    re = Relationship(node_q, "CONNECTED", prefix_q, **connected)
                    if re is None:
                        print("issue to create a relationship between {} & {}".format(node_q, prefix_q))
                    else:
                        create_attached_link(re)







def main():
    db_isis = create_dict_from_xml(filename)
    create_topology_from_dict(lsas=db_isis)

    # print(db_isis)


if __name__ == "__main__":
    main()
