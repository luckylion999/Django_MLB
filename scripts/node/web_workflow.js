#!/usr/bin/env node


/*
 *
 * npm install request
 * npm install node-uuid
*/

var request = require('request');
var uuid = require('node-uuid');
var uuid1 = uuid.v4();
var username = uuid1.substring(0,20) + "@test.com";

/*
 * Create a user, passing email address as username, and also as email.
 * For demo, use 'default' for password
 */
request.post('http://localhost:8000/users/', {
    headers: {
        'Authorization': 'Token ecc8a2a0412c154e78f94f4b4aa573b1a56fe661'
    },
    form: {
        'username': username,
        'email': username,
        'password':'default',
    },
    json: true}, function(err, res, body) {
        console.log('Create User returned:');
        console.log(err, res.body);

        /*
         * Get user token
         * Arguments:
         * username
         * password
         * requires 3Pak API token for access
         * curl --data "username=username&password=password" https://code.3pakapi.net/api-token-auth/
         */

        request.post('http://localhost:8000/api-token-auth/', {
            headers: {
                'Authorization': 'Token ecc8a2a0412c154e78f94f4b4aa573b1a56fe661'
            },
            form: {
                'username': username,
                'password':'default',
            },
            json: true}, function(err, res, body) {
                  console.log('Get User Token returned:');
                  console.log(err, res.body);
                  var mytoken = "token " + res.body.token;
                  console.log(mytoken);

                  /*
                   * Load the player game records
                   *
                   * Important: note that we now use mytoken, which embeds the user's account identity
                   *
                   * curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" https://code.3pakapi.net/playergames/
                   */

                  request.get('http://localhost:8000/playergames/', {
                      headers: {
                          'Authorization': mytoken
                      },
                      json: true}, function(err, res, body) {
                            console.log('Player Games returned:');
                            var results = res.body.results;
                            console.log(err, results);
                            console.log(err, res.body.count);

                  });
                  /*
                   * The same would be done to pull team games (defense
                   * request.get('http://localhost:8000/teamgames/'...
                   */
        });
});




/*
request.post('http://localhost:8000/is_pick_window_open;', {json: true}, function(err, res, body) {
          console.log(err, res);
});
*/
