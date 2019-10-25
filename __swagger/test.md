swagger: '2.0'
info:
  description: 'rr b2c'
  version: '1.0.0'
  title: 'rr b2c'
  contact:
    email: 'rahuldbhadange.com'
host: 'localhost:8080'
basePath: '/'
schemes:
  - 'https'
  - 'http'
paths:  
  /ron/{asset_id}:
    post:
      summary: 'Find ron data by asset ID and time'
      description: 'Returns sample event list json'
      operationId: 'get_ron_data_by_asset_id_and_time_desc'
      produces:
        - 'application/xml'
        - 'application/json'
      parameters:
      - name: 'asset_id'
        in: 'path'
        description: 'ID of asset to return'
        required: true
        type: 'string'
      - name: 'query'
        in: 'body'
        description: 'query parameter to fetch required doc'
        required: true
        schema:
          $ref: '#/definitions/RonQuery'
      responses:
        200:
          description: 'successful operation'
        400:
          description: 'Invalid ID supplied'
        404:
          description: 'Asset not found'
      x-swagger-router-controller: 'rrps.dt.follower.rest_follower.controllers.default_controller'


definitions:
  RonQuery:
    properties:
      start:
        type: 'string'
      end:
        type: 'string'
      description:
        type: 'array'
        items:
          type: 'string'
      start_limit:
        type: 'integer'
      end_limit:
        type: 'integer'
        
        
        
        
        
        
        
        
        
        
        






































{"start": "2013-03-02", "end":"2019-03-02", "start_limit":5, "end_limit": 188,
"description":["FSW Version", "BoM as built set", "Technical Document"]}

swagger 2.0
title : 'gspm'
host : 'localhost:2701'
basepath : '/'
consumer : 'application/xml'
path : 
    ron/{asset_id}:
        post:
            parameters:
                name : 'asset_id'
                in : 'path'
                description : 'desc'
                type : 'string'
                required : true
                name : 'query'
                in : 'body'
                description: 'desc'
                required: true
                schema :
                     $ref: '#/definitions/RonQuery'
                    
definitions:               
    RonQuery:
        properties:
            limit :
                type : 'integer'
            start :
                type : 'string'
            stop :
                type : 'string'
            description :
                type : 'array'
                items :
                    type : 'string'
            
                
                        
                
                    
                
    