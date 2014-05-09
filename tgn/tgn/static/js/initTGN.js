var tgn = angular.module('angularTGN', ['ngRoute']);

tgn.config(
    function ($controllerProvider, $provide, $compileProvider, $routeProvider) {

        console.log("Config method executed.");

        tgn._controller = tgn.controller;
        tgn._service = tgn.service;
        tgn._factory = tgn.factory;
        tgn._value = tgn.value;
        tgn._directive = tgn.directive;

        tgn.controller = function (name, constructor) {

            $controllerProvider.register(name, constructor);
            return( this );

        };

        tgn.service = function (name, constructor) {

            $provide.service(name, constructor);
            return( this );

        };

        tgn.factory = function (name, factory) {

            $provide.factory(name, factory);
            return( this );

        };

        tgn.value = function (name, value) {

            $provide.value(name, value);
            return( this );

        };

        tgn.directive = function (name, factory) {

            $compileProvider.directive(name, factory);
            return( this );

        };

        // Set our routes here
        $routeProvider
            .when('/', {
                templateUrl: 'partials/login'
            })
            .when('/myProfile', {
                templateUrl: 'partials/myProfile'
            })
            .when('/otherProfile/:otherProfile', {
                templateUrl: 'partials/otherProfile'
            })
            .when('/myNonprofit/:myNonprofit', {
                templateUrl: 'partials/myNonprofit'
            })
            .when('/otherNonprofit/:otherNonprofit', {
                templateUrl: 'partials/otherNonprofit'
            })
            .when('/myJob/:jobId/:jobType', {
                templateUrl: 'partials/myJob',
                controller: 'viewMyJobController'
            })
            .when('/jobApplicants', {
                templateUrl: 'partials/jobApplicants'
            })
            .when('/searchResults/:search', {
                templateUrl: 'partials/searchResults'
            })


            .otherwise({redirectTo: '/'});
    }
);

tgn.factory('myProfileService', function () {
    var userModel = {
        accessToken: '',
        userId: '',
        name: '',
        aboutMe: '',
        resume: '',
        profileImageUrl: '',
        titles: [],
        skills: []
    };

    var loggedIn = false;

    var myProfileService = {}

    myProfileService.login = function (user) {
        for (attribute in user) {
            userModel[attribute] = user[attribute]
        }

        loggedIn = true;
    };

    myProfileService.logout = function () {
        userModel.accessToken = '';
        userModel.userId = '';
        userModel.name = '';
        userModel.aboutMe = '';
        userModel.resume = '';
        userModel.profileImageUrl = '';
        userModel.titles = [];
        userModel.skills = [];

        loggedIn = false;
    };

    myProfileService.updateModel = function (newModel) {
        for (updatedAttribute in newModel) {
            userModel[updatedAttribute] = newModel[updatedAttribute]
        }
    };

    myProfileService.userModel = function () {
        return userModel;
    };

    myProfileService.isLoggedIn = function () {
        return loggedIn;
    };

    return myProfileService;
});
tgn.factory('myNonprofitsService', function () {
    var myNonprofits = [];

    var myNonprofitsService = {};

    myNonprofitsService.setMyNonprofits = function (nonprofits) {
        myNonprofits = nonprofits.splice(0);
    };

    myNonprofitsService.updateNonprofit = function (nonprofitId, updatedNonprofitModel) {
        for (var i = 0, j = myNonprofits.length; i < j; i++) {
            if (myNonprofits[i].nonprofitId == nonprofitId) {
                for (updatedAttribute in updatedNonprofitModel) {
                    myNonprofits[i][updatedAttribute] = updatedNonprofitModel[updatedAttribute]
                }
                break;
            }
        }
    };

    myNonprofitsService.getNonprofit = function (nonprofitId) {
        for (var i = 0, j = myNonprofits.length; i < j; i++) {
            if (myNonprofits[i]['nonprofitId'] == nonprofitId) {
                return myNonprofits[i];
            }
        }
    };

    myNonprofitsService.myNonprofits = function () {
        return myNonprofits;
    };

    myNonprofitsService.addNonprofit = function (newNonprofit) {
        myNonprofits = myNonprofits.concat(newNonprofit);
    };

    return myNonprofitsService;
});

tgn.factory('myJobsService', function () {
    var myJobs = {
        jobsAsApplicant: [],
        currentJobsAsEmployee: [],
        completedJobsAsEmployee: []
    };

    var myJobsService = {};

    myJobsService.setMyJobs = function (jobs) {
        myJobs = jobs;
    };

    myJobsService.setMyApplications = function (applications) {
        myJobs['jobsAsApplicant'] = applications;
    };

    myJobsService.setMyCurrentJobs = function (currentJobs) {
        myJobs['currentJobsAsEmployee'] = currentJobs;
    };

    myJobsService.setMyCompletedJobs = function (completedJobs) {
        myJobs['completedJobsAsEmployee'] = completedJobs
    };

    myJobsService.getJob = function (jobId, jobType) {
        for (var i = 0, j = myJobs[jobType].length; i < j; i++) {
            if (myJobs[jobType][i]['jobId'] == jobId) {
                return myJobs[jobType][i];
            }
        }
    };

    myJobsService.myJobs = function () {
        return myJobs
    };

    return myJobsService
});


tgn.controller('userController', function ($scope, myProfileService, myNonprofitsService, myJobsService) {
    $scope.myProfile = myProfileService;
    $scope.myNonprofits = myNonprofitsService;
    $scope.myJobs = myJobsService;
});


tgn.controller('editProfileController', function ($scope) {
    
    $scope.newModel = {}
    $scope.newModel.skills = $scope.myProfile.userModel().skills.slice(0);
    $scope.newModel.titles = $scope.myProfile.userModel().titles.slice(0);
    
    $scope.newModel.aboutMe = $scope.myProfile.userModel().aboutMe;
    $scope.newModel.resume = $scope.myProfile.userModel().resume;

    $scope.addSkill = function (skill) {
        if (skill.length > 0 &&
            $scope.newModel.skills.indexOf(skill) == -1) {
            $scope.newSkill = "";
            $scope.newModel.skills.push(skill);
            console.log($scope.newModel.skills);
        }
    };

    $scope.addTitle = function (title) {
        $scope.newModel.titles.push(title);
    };

    $scope.removeSkill = function (skill) {
        console.log($scope.newModel.skills);
        var index = $scope.newModel.skills.indexOf(skill);
        $scope.newModel.skills.splice(index, 1);
        console.log($scope.newModel.skills);

    };

    $scope.removeTitle = function (title) {
        $scope.newModel.titles.remove(title);
    };

    $scope.resetSkillsAndTitles = function () {
        $scope.newModel.skills = $scope.myProfile.userModel().skills.slice(0);
        $scope.newModel.titles = $scope.myProfile.userModel().titles.slice(0);
    };
});

var initTGN = function (accessToken) {
    tgn.value('accessToken', accessToken);

    tgn.factory('searchResultsService', function () {
        var search = {
            postedJobs: [],
            nonprofits: [],
            otherUsers: [],
            query: ''
        };

        var searchService = {};

        searchService.setPostedJobs = function (postedJobs) {
            search.postedJobs = postedJobs;
        };

        searchService.setNonprofits = function (nonprofits) {
            search.nonprofits = nonprofits;
        };

        searchService.setOtherUsers = function (otherUsers) {
            search.otherUsers = otherUsers;
        };

        searchService.setQuery = function (query) {
            search.query = query;
        };

        searchService.searchResults = function () {
            return search;
        };

        return searchService
    });

    tgn.factory('viewContentService', function () {
        var nonprofitToView = {
            nonprofitId: '',
            name: '',
            mission: '',
            description: '',
            website: '',
            address: '',
            jobs: {
                postedJobs: [],
                currentJobs: [],
                completedJobs: []
            },
            affiliates: []
        };

        var otherUserToView = {
            userId: '',
            name: '',
            aboutMe: '',
            profileImageUrl: '',
            resume: '',
            titles: [],
            skills: [],
            jobs: {
                jobsAsApplicant: [],
                currentJobsAsEmployee: [],
                completedJobsAsEmployee: []
            },
            nonprofits: []
        };

        var jobToView = {
            jobId: '',
            name: '',
            nonprofitId: '',
            nonprofitName: '',
            titles: [],
            description: '',
            compensation: '',
            city: '',
            state: '',
            jobType: '',
            timeCreated: '',
            skills: []
        };

        var viewContent = {
            nonprofitToView: nonprofitToView,
            otherUserToView: otherUserToView,
            jobToView: jobToView
        };

        var viewContentService = {};

        viewContentService.setNonprofitToView = function (nonprofit) {
            nonprofitToView = nonprofit;
        };

        viewContentService.setOtherUserToView = function (otherUser) {
            otherUserToView = otherUser
        };

        viewContentService.setJobToView = function (job) {
            jobToView = job;
        };

        viewContentService.viewContent = function () {
            return viewContent
        };

        return viewContentService;
    });

    tgn.factory('requestService', function ($http, accessToken) {
            var requestService = {};
            var accessToken = accessToken;
            var getResponseData = function (response) {
                console.log('got response:  ' + JSON.stringify(response))
                return response.data;
            };
            var makePostRequest = function (url, parameters) {
                console.log("making post request with: " + JSON.stringify(parameters));


                return $http.post(url, parameters, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }).then(function (response) {
                    return getResponseData(response);
                })
            };
            var requestPrefix = '/tgn/api/';

            requestService.loginWithFacebook = function (myProfileService, myNonprofitsService, myJobsService) {
                var requestUrl = requestPrefix + 'loginWithFacebook';
                var requestArgs = {
                    accessToken: accessToken
                };

                makePostRequest(requestUrl, requestArgs).then(function (responseData) {
                    var loginInfo = responseData.data.me;

                    if (loginInfo) {
                        console.log('logging in ' + JSON.stringify(loginInfo));

                        var newProfileModel = {
                            accessToken: accessToken,
                            userId: loginInfo['userId'],
                            profileImageUrl: loginInfo['profileImageUrl'],
                            skills: loginInfo['skills'],
                            titles: loginInfo['titles'],
                            resume: loginInfo['resume'],
                            aboutMe: loginInfo['aboutMe'],
                            name: loginInfo['name']
                        };
                        myProfileService.login(newProfileModel);

                        var newJobsModel = loginInfo['jobs'];
                        myJobsService.setMyJobs(newJobsModel);

                        var newNonprofitsModel = loginInfo['nonprofits']
                        console.log(JSON.stringify(newNonprofitsModel));
                        myNonprofitsService.setMyNonprofits(newNonprofitsModel);
                    } else {
                        console.log(responseData.errorMessage);
                    }
                });

            };

            requestService.updateProfile = function (myProfileService, newModel) {
                var requestUrl = requestPrefix + 'updateProfile';

                myProfileService.updateModel(newModel['profile']);
                console.log('posting to update profile with:  ' + JSON.stringify(newModel));
                
                makePostRequest(requestUrl, newModel).then(function (responseData) {
                    
                    
                    var updatedProfile = responseData.data.updatedProfile;

                    if (updatedProfile) {
                        myProfileService.updateModel(updatedProfile);
                    } else {
                        console.log(responseData.errorMessage);
                    }
                });
            };
        
        
            //CREATE NEW JOB REQUEST
            requestService.addNonprofitJob = function (userId, nonprofitId, newJob) {
                var requestUrl = requestPrefix + 'postJobAsNonprofit';
                var data = {
                    'userId': userId,
                    'nonprofitId': nonprofitId,
                    'jobToPost': newJob
                }
                console.log('posting to addJobAsNonprofit with: ' + JSON.stringify(data));
                makePostRequest(requestUrl, data).then(function (responseData)
                    {
                        console.log("printing response data from job creation: " + responseData.data);
                        console.log(responseData.errorMessage);
                    }
                )
            };

            //CREATE NEW NONPROFIT REQUEST
            requestService.createNonprofit = function (myProfileService, myNonprofitsService, newNonprofit) {
                console.log('called create nonprofit for: ' + JSON.stringify(newNonprofit));
                var requestUrl = requestPrefix + 'createNonprofit';

                var createNonprofitRequestObject = {
                    userId: myProfileService.userModel().userId,
                    nonprofit: newNonprofit
                };

                makePostRequest(requestUrl, createNonprofitRequestObject).then(function (responseData) {
                    var newNonprofit = responseData.data.newNonprofit;
                    var myNonprofits = responseData.data.myNonprofits;

                    if (myNonprofits) {
                        myNonprofitsService.setMyNonprofits(myNonprofits);
                        window.location = '#/myNonprofit/' + newNonprofit.nonprofitId
                    } else {
                        console.log(responseData.errorMessage)
                    }
                });
            };
        
            //EDIT NONPROFIT PROFILE REQUEST
//            requestService.editNonprofit = function(myProfileService, myNonprofitsService, nonprofit) {
//                console.log('called edit nonprofit for: ' + JSON.stringify(nonprofit));
//                
//                var requestUrl = requestPrefix + 'editNonprofit';
//                
//                var editNonprofitRequestObject = {
//                    userId: myProfileService.userModel().userId,
//                    nonprofit: nonprofit;
//                }
//                
//                makePostRequest(requestUrl, editNonprofitRequestObject).then(function (responseData) {
//                    //Set nonprofit profile model info here
//                    
//                    
//                });
//                
//            };
        
            return requestService;
        }
    );

    tgn.controller('TGNController', function ($scope, searchResultsService, viewContentService, requestService) {
        $scope.searchResults = searchResultsService;
        $scope.viewContent = viewContentService;
        $scope.requestService = requestService;
        console.log('made the controller');
        $scope.requestService.loginWithFacebook($scope.myProfile, $scope.myNonprofits, $scope.myJobs);
    });


    tgn.controller('createNonprofitController', function ($scope, requestService) {
        $scope.newNonprofit = {};
        $scope.requestService = requestService;
    });

    tgn.controller('createNewJobController', function ($scope, requestService, myProfileService) {
        $scope.newJob = {};
        $scope.myProfile = myProfileService;
        $scope.requestService = requestService;
        $scope.newJob.skills = [];
        $scope.newJob.titles = [];

        $scope.addSkill = function (skill) {
            if (skill.length > 0 &&
                $scope.newJob.skills.indexOf(skill) == -1) {
                $scope.newSkill = "";
                $scope.newJob.skills.push(skill);
                console.log($scope.newJob.skills);
            }
        };

        $scope.removeSkill = function (skill) {
            console.log($scope.newJob.skills);
            var index = $scope.newJob.skills.indexOf(skill);
            $scope.newJob.skills.splice(index, 1);
            console.log($scope.newJob.skills);
        };

        $scope.addTitle = function (title) {
            if (title.length > 0 &&
                $scope.newJob.titles.indexOf(title) == -1) {
                $scope.newTitle = "";
                $scope.newJob.titles.push(title);
                console.log($scope.newJob.titles);
            }
        };

        $scope.removeTitle = function (title) {
            console.log($scope.newJob.titles);
            var index = $scope.newJob.titles.indexOf(title);
            $scope.newJob.titles.splice(index, 1);
            console.log($scope.newJob.titles);
        };



    });

    tgn.controller('viewMyJobController', function ($scope, myJobsService, $routeParams) {
        $scope.myJob = myJobsService.getJob($routeParams.jobId, $routeParams.jobType);
    });

    tgn.controller('viewMyNonprofitController', function ($scope, $routeParams, $location, $anchorScroll) {
        
        $scope.goToJobs = function() {
            $location.hash('jobAnchor');
            $anchorScroll();
        }
        
        console.log('got routeParams ' + JSON.stringify($routeParams));
        $scope.myNonprofit = $scope.myNonprofits.getNonprofit($routeParams.myNonprofit);
        console.log('my nonprofit: ' + JSON.stringify($scope.myNonprofit));
    });
};
