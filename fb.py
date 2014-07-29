#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   26/07/2014

import requests
import pandas as pd
import os

def get_fb( sub_domain='me', params={} ):
    base_url = 'https://graph.facebook.com/v2.0/'
    if params.has_key('access_token') == False:
        params['access_token']='CAACEdEose0cBALCXPu9Ynihn7sa8gjhkIDoPyF8Fko1IP70QsTGuqlAvazzCg7Rc7KL9w28BSixghoCIPLZCZCtPkfCuLwH9gnxLVfQFuBA0GVKknKqnSe8LtptRteZBcph5j3QKZCFH7fOXHKreSl7V9Przzg16VD811bccYW1ZCSxGRRGvAFSRuWTX0Bwq7JMHvvnsbogZDZD'
    base_url = base_url + sub_domain
    return requests.get( base_url, params=params ).json()


def get_node_id( nodename='' ):
    base_url = 'https://graph.facebook.com/' + nodename
    return requests.get( base_url ).json()['id']


def file_path( nodeid, edgetype, project ):
    """ Assign the filepath created using nodeid and edgetype to path """
    fname = str(nodeid) + '_' + edgetype + '.json'
    dirsep = os.path.sep
    path = os.getcwd() + dirsep + 'data' + dirsep + project + dirsep + fname
    return path
    
    
def get_edges( nodeid, edgetype, project ):
    """ Pull all the edges of type edgetype of node identified by
        nodeid"""
    nodeid = str(nodeid)
    path = file_path( nodeid, edgetype, project )
    if os.path.isfile( path ):
        return pd.read_json( path )
    
    print 'Downloading data: ' + edgetype
    subdomain = nodeid + '/' + edgetype
    fbresponse = get_fb( subdomain )
    if fbresponse.has_key('error'):
        print 'Error occurred'
        return fbresponse['error']

    data_list = fbresponse['data']
    
    params = {}
    params['limit'] = 50
    while fbresponse.has_key('paging') and \
          fbresponse['paging'].has_key('cursors'):
        params['after'] = fbresponse['paging']['cursors']['after']
        fbresponse = get_fb( subdomain, params )
        if fbresponse.has_key('data'):
            data_list.extend( fbresponse['data'] )
            print '.'
    
    if data_list[-1:] == [[]]:
        data_list.pop()
        
    print '\nData download complete.'
    
    fwrite = open( path, 'w' )
    
    data_list.reverse() # .reverse() returns None
    df = pd.DataFrame( data_list )
    df.to_json( fwrite )
    fwrite.close()
    return df


class FbNode():
    def __init__( self, nodeid, projectname ):
        self.project_ = projectname
        self.id_ = nodeid
        
        
    def allLikes(self):
        self.likes_ = get_edges( self.id_, 'likes', self.project_ )
        return self.likes_
        
        
    def allComments(self):
        self.comments_ = get_edges( self.id_, 'comments', self.project_ )
        if self.comments_.columns.size == 0:
            return self.comments_
        return self.comments_['message']
    
    
    def allComUsers(self):
        self.comments_ = get_edges( self.id_, 'comments', self.project_ )
        if self.comments_.columns.size == 0:
            return self.comments_
            
        return self.comments_['from']
       
       
    def allUsers(self):
        path = file_path( self.id_, 'user', self.project_ )
        if os.path.isfile( path ):
            self.users_ = pd.read_json( path )
            return self.users_
            
        comusers = self.comments_['from'].tolist()#converting a
                                                # Series of dict to list of dict
        userslist = comusers.extend(self.likes_.to_dict('record'))
        self.users_ = pd.DataFrame( userlist )
        self.users_.to_json( path )
        return self.users
        
       
    
class FbPageNode():
    def __init__( self, projectname ):
        self.project_ = projectname
        self.id_ = get_node_id( projectname )
        
        
    def allLinks( self ):
        self.links_ = get_edges( self.id_, 'links', self.project_ )
        return self.links_
    
    
    def allLikes( self ):
        path = file_path( self.id_, 'likes', self.project_ )
        if os.path.isfile( path ):
            print 'its reading from file'
            self.likes_ = pd.read_json( path )
            return self.likes_
            
        self.links_ = get_edges( self.id_, 'links', self.project_ )
        linkids = self.links_['id']
        fwrite = open( path, 'a' )
        for ids in linkids:
            linknode = FbNode( ids, self.project_ )
            linknode.allLikes().to_csv( fwrite, mode='a', sep='\t',\
                                        index=False, encoding='utf8' )
        fwrite.close()
        self.likes_ = pd.read_csv( path, sep='\t', encoding='utf8' )
        self.likes_.to_json( path )
        return self.likes_
    
    
    def allComments( self ):
        path = file_path( self.id_, 'comments', self.project_ )
        if os.path.isfile( path ):
            self.comments_ = pd.read_json( path )
            return self.comments_
            
        self.links_ = get_edges( self.id_, 'links', self.project_ )
        linkids = self.links_['id']
        fwrite = open( path, 'a' )
        for ids in linkids:
            linknode = FbNode( ids, self.project_ )
            linknode.allComments().to_csv( fwrite, mode='a', sep='\t',\
                                           index=False, encoding='utf8' )
        fwrite.close()
        self.comments_ = pd.read_csv( path,sep='\t', encoding='utf8')
        self.comments_.to_json( path )
        return self.comments_ 
        
        
    def allUsers( self ):
        path = file_path( self.id_, 'users', self.project_ )
        if os.path.isfile( path ):
            self.users_ = pd.read_json( path )
            return self.users_
        
        self.links_ = get_edges( self.id_, 'links', self.project_ )
        linkids = self.links_['id']
        fwrite = open( path, 'a' )
        for ids in linkids:
            linknode = FbNode( ids, self.project_ )
            linknode.allUsers().to_csv( fwrite, mode='a', sep='\t',\
                                        index=False, encoding='utf8' )
        fwrite.close()
        self.users_ = ( pd.read_csv( path, sep='\t' ,encoding='utf8' ) )
        self.users_.to_json( path )
        return self.users_
        
        
        
        
    
