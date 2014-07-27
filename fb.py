#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   26/07/2014

import requests
import pandas as pd

def get_fb( sub_domain='me', params={} ):
    base_url = 'https://graph.facebook.com/v2.0/'
    if params.has_key('access_token') == False:
        params['access_token']='CAACEdEose0cBALCXPu9Ynihn7sa8gjhkIDoPyF8Fko1IP70QsTGuqlAvazzCg7Rc7KL9w28BSixghoCIPLZCZCtPkfCuLwH9gnxLVfQFuBA0GVKknKqnSe8LtptRteZBcph5j3QKZCFH7fOXHKreSl7V9Przzg16VD811bccYW1ZCSxGRRGvAFSRuWTX0Bwq7JMHvvnsbogZDZD'
    base_url = base_url + sub_domain
    return requests.get( base_url, params=params ).json()


def get_node_id( nodename='' ):
    base_url = 'https://graph.facebook.com/' + nodename
    return requests.get( base_url ).json()['id']


def get_edges( nodeid=None, edgetype='', nodename=None ):
    """ Pull all the edges of type edgetype of node identified by
        nodeid"""
    if nodeid == None:
        return
    
    print 'Downloading data.'
    subdomain = nodeid + '/' + edgetype
    fbresponse = get_fb( subdomain )
    data_list = fbresponse['data']
    
    params = {}
    params['limit'] = 25
    while fbresponse.has_key('paging') and \
          fbresponse['paging'].has_key('cursors'):
        params['after'] = fbresponse['paging']['cursors']['after']
        fbresponse = get_fb( subdomain, params )
        data_list.extend( fbresponse['data'] )
        print '.'
    
    if data_list[-1:] == [[]]:
        data_list.pop()
        
    print '\nData download complete.'
    if nodename != None:
        fname = nodename + '_' + edgetype + '.txt'
    else:
        fname = nodeid + '_' + edgetype + '.txt'
    fwrite = open( fname, 'w' )
    
    data_list.reverse() # .reverse() returns None
    df = pd.DataFrame( data_list )
    df.to_csv( fwrite, sep='\t', index=False, encoding='utf8' )
    return df

class FbNode():
    def __init__( self, nodename ):
        self.name_ = nodename
        self.id_ = get_node_id( self.name_ )
    def allLikes()
    def allComments()
    def allComUsers()
    def allUsers()
    def updateNode()
       
    
class FbPageNode(FbNode):
    
    def getAllLinks():
        return get_edges( self.id_, 'links', self.name_ )
    def allLinks()
    
        
        
        
        
    
