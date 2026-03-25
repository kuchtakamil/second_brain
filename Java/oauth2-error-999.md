# OAuth2 Error 999

**Data:** 2024-05-04

---

**User:**

I try to create simple java + spring security application to login using OAuth2.
I get the following logs and error with status code 999
Trying to match request against DefaultSecurityFilterChain [RequestMatcher=any request, Filters=[org.springframework.security.web.session.DisableEncodeUrlFilter@2954f6ab, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@58fbd02e, org.springframework.security.web.context.SecurityContextHolderFilter@fb49fdf, org.springframework.security.web.header.HeaderWriterFilter@5b5dce5c, org.springframework.web.filter.CorsFilter@163042ea, org.springframework.security.web.csrf.CsrfFilter@bfec2f9, org.springframework.security.web.authentication.logout.LogoutFilter@32a2a6be, org.springframework.security.oauth2.client.web.OAuth2AuthorizationRequestRedirectFilter@58af5076, org.springframework.security.oauth2.client.web.OAuth2LoginAuthenticationFilter@7a3b7122, org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter@58b5a2f3, org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter@309cedb6, org.springframework.security.web.authentication.ui.DefaultLogoutPageGeneratingFilter@11d045b4, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@7da34b26, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@10c47c79, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@1fbf088b, org.springframework.security.web.access.ExceptionTranslationFilter@273a5a8a, org.springframework.security.web.access.intercept.AuthorizationFilter@3252747e]] (1/1)
Securing GET /oauth2/authorization/google
Invoking DisableEncodeUrlFilter (1/17)
Invoking WebAsyncManagerIntegrationFilter (2/17)
Invoking SecurityContextHolderFilter (3/17)
Invoking HeaderWriterFilter (4/17)
Invoking CorsFilter (5/17)
Invoking CsrfFilter (6/17)
Did not protect against CSRF since request did not match CsrfNotRequired [TRACE, HEAD, GET, OPTIONS]
Invoking LogoutFilter (7/17)
Did not match request to Ant [pattern='/logout', POST]
Invoking OAuth2AuthorizationRequestRedirectFilter (8/17)
Redirecting to https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com&scope=openid%20profile%20email&state=9gbfouzk1DZ21WKvk8iJRXXA5fF5UZo1pIQgiIkdV6M%3D&redirect_uri=http://localhost:8080/login/oauth2/code/google&nonce=7d9jDo6OpQZGveB4WJkTOHVj1eSnS7igpnDkFO_GBZw
Not injecting HSTS header since it did not match request to [Is Secure]
Trying to match request against DefaultSecurityFilterChain [RequestMatcher=any request, Filters=[org.springframework.security.web.session.DisableEncodeUrlFilter@2954f6ab, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@58fbd02e, org.springframework.security.web.context.SecurityContextHolderFilter@fb49fdf, org.springframework.security.web.header.HeaderWriterFilter@5b5dce5c, org.springframework.web.filter.CorsFilter@163042ea, org.springframework.security.web.csrf.CsrfFilter@bfec2f9, org.springframework.security.web.authentication.logout.LogoutFilter@32a2a6be, org.springframework.security.oauth2.client.web.OAuth2AuthorizationRequestRedirectFilter@58af5076, org.springframework.security.oauth2.client.web.OAuth2LoginAuthenticationFilter@7a3b7122, org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter@58b5a2f3, org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter@309cedb6, org.springframework.security.web.authentication.ui.DefaultLogoutPageGeneratingFilter@11d045b4, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@7da34b26, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@10c47c79, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@1fbf088b, org.springframework.security.web.access.ExceptionTranslationFilter@273a5a8a, org.springframework.security.web.access.intercept.AuthorizationFilter@3252747e]] (1/1)
Securing GET /login/oauth2/code/google?state=9gbfouzk1DZ21WKvk8iJRXXA5fF5UZo1pIQgiIkdV6M%3D&code=4%2F0AdLIrYcMD7LYg9mhE35nuNIIUi7Gmaiw8t2ifNPniCe7GaJwZixBQ9h6mLOjTdtl_GYNZg&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=consent
Invoking DisableEncodeUrlFilter (1/17)
Invoking WebAsyncManagerIntegrationFilter (2/17)
Invoking SecurityContextHolderFilter (3/17)
Invoking HeaderWriterFilter (4/17)
Invoking CorsFilter (5/17)
Invoking CsrfFilter (6/17)
Did not protect against CSRF since request did not match CsrfNotRequired [TRACE, HEAD, GET, OPTIONS]
Invoking LogoutFilter (7/17)
Did not match request to Ant [pattern='/logout', POST]
Invoking OAuth2AuthorizationRequestRedirectFilter (8/17)
Invoking OAuth2LoginAuthenticationFilter (9/17)
Authenticating request with OAuth2LoginAuthenticationProvider (1/3)
Authenticating request with OidcAuthorizationCodeAuthenticationProvider (2/3)
Preparing session with ChangeSessionIdAuthenticationStrategy (1/2)
Changed session id from F8D87A2A561577B39AE416F781269480
Preparing session with CsrfAuthenticationStrategy (2/2)
Replaced CSRF Token
Stored SecurityContextImpl [Authentication=OAuth2AuthenticationToken [Principal=Name: [116396123335717576796], Granted Authorities: [[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]], User Attributes: [{at_hash=8c4_6SnlseoVm9WZqlA6WQ, sub=116396123335717576796, email_verified=true, iss=https://accounts.google.com, given_name=Kamil, nonce=7d9jDo6OpQZGveB4WJkTOHVj1eSnS7igpnDkFO_GBZw, picture=https://lh3.googleusercontent.com/a/ACg8ocJ9CV8HJxfxYqHdvHGJLXlpfdEhwmtlLOdrSG3lRS6MrdmIMw=s96-c, aud=[75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com], azp=75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com, name=Kamil, exp=2024-05-04T10:48:48Z, iat=2024-05-04T09:48:48Z, email=kuchtakamil@gmail.com}], Credentials=[PROTECTED], Authenticated=true, Details=WebAuthenticationDetails [RemoteIpAddress=0:0:0:0:0:0:0:1, SessionId=F8D87A2A561577B39AE416F781269480], Granted Authorities=[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]]] to HttpSession [org.apache.catalina.session.StandardSessionFacade@689af911]
Set SecurityContextHolder to OAuth2AuthenticationToken [Principal=Name: [116396123335717576796], Granted Authorities: [[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]], User Attributes: [{at_hash=8c4_6SnlseoVm9WZqlA6WQ, sub=116396123335717576796, email_verified=true, iss=https://accounts.google.com, given_name=Kamil, nonce=7d9jDo6OpQZGveB4WJkTOHVj1eSnS7igpnDkFO_GBZw, picture=https://lh3.googleusercontent.com/a/ACg8ocJ9CV8HJxfxYqHdvHGJLXlpfdEhwmtlLOdrSG3lRS6MrdmIMw=s96-c, aud=[75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com], azp=75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com, name=Kamil, exp=2024-05-04T10:48:48Z, iat=2024-05-04T09:48:48Z, email=kuchtakamil@gmail.com}], Credentials=[PROTECTED], Authenticated=true, Details=WebAuthenticationDetails [RemoteIpAddress=0:0:0:0:0:0:0:1, SessionId=F8D87A2A561577B39AE416F781269480], Granted Authorities=[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]]
Redirecting to http://localhost:8080/error?continue
Not injecting HSTS header since it did not match request to [Is Secure]
Trying to match request against DefaultSecurityFilterChain [RequestMatcher=any request, Filters=[org.springframework.security.web.session.DisableEncodeUrlFilter@2954f6ab, org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter@58fbd02e, org.springframework.security.web.context.SecurityContextHolderFilter@fb49fdf, org.springframework.security.web.header.HeaderWriterFilter@5b5dce5c, org.springframework.web.filter.CorsFilter@163042ea, org.springframework.security.web.csrf.CsrfFilter@bfec2f9, org.springframework.security.web.authentication.logout.LogoutFilter@32a2a6be, org.springframework.security.oauth2.client.web.OAuth2AuthorizationRequestRedirectFilter@58af5076, org.springframework.security.oauth2.client.web.OAuth2LoginAuthenticationFilter@7a3b7122, org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter@58b5a2f3, org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter@309cedb6, org.springframework.security.web.authentication.ui.DefaultLogoutPageGeneratingFilter@11d045b4, org.springframework.security.web.savedrequest.RequestCacheAwareFilter@7da34b26, org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter@10c47c79, org.springframework.security.web.authentication.AnonymousAuthenticationFilter@1fbf088b, org.springframework.security.web.access.ExceptionTranslationFilter@273a5a8a, org.springframework.security.web.access.intercept.AuthorizationFilter@3252747e]] (1/1)
Securing GET /error?continue
Invoking DisableEncodeUrlFilter (1/17)
Invoking WebAsyncManagerIntegrationFilter (2/17)
Invoking SecurityContextHolderFilter (3/17)
Invoking HeaderWriterFilter (4/17)
Invoking CorsFilter (5/17)
Invoking CsrfFilter (6/17)
Did not protect against CSRF since request did not match CsrfNotRequired [TRACE, HEAD, GET, OPTIONS]
Invoking LogoutFilter (7/17)
Did not match request to Ant [pattern='/logout', POST]
Invoking OAuth2AuthorizationRequestRedirectFilter (8/17)
Invoking OAuth2LoginAuthenticationFilter (9/17)
Did not match request to Ant [pattern='/login/oauth2/code/*']
Invoking UsernamePasswordAuthenticationFilter (10/17)
Did not match request to Ant [pattern='/login', POST]
Invoking DefaultLoginPageGeneratingFilter (11/17)
Invoking DefaultLogoutPageGeneratingFilter (12/17)
Did not render default logout page since request did not match [Ant [pattern='/logout', GET]]
Invoking RequestCacheAwareFilter (13/17)
Removing DefaultSavedRequest from session if present
Loaded matching saved request http://localhost:8080/error?continue
Invoking SecurityContextHolderAwareRequestFilter (14/17)
Invoking AnonymousAuthenticationFilter (15/17)
Invoking ExceptionTranslationFilter (16/17)
Invoking AuthorizationFilter (17/17)
Authorizing SecurityContextHolderAwareRequestWrapper[ org.springframework.security.web.savedrequest.SavedRequestAwareWrapper@4d17d6df]
Checking authorization on SecurityContextHolderAwareRequestWrapper[ org.springframework.security.web.savedrequest.SavedRequestAwareWrapper@4d17d6df] using org.springframework.security.authorization.AuthenticatedAuthorizationManager@5fbaf034
Retrieved SecurityContextImpl [Authentication=OAuth2AuthenticationToken [Principal=Name: [116396123335717576796], Granted Authorities: [[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]], User Attributes: [{at_hash=8c4_6SnlseoVm9WZqlA6WQ, sub=116396123335717576796, email_verified=true, iss=https://accounts.google.com, given_name=Kamil, nonce=7d9jDo6OpQZGveB4WJkTOHVj1eSnS7igpnDkFO_GBZw, picture=https://lh3.googleusercontent.com/a/ACg8ocJ9CV8HJxfxYqHdvHGJLXlpfdEhwmtlLOdrSG3lRS6MrdmIMw=s96-c, aud=[75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com], azp=75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com, name=Kamil, exp=2024-05-04T10:48:48Z, iat=2024-05-04T09:48:48Z, email=kuchtakamil@gmail.com}], Credentials=[PROTECTED], Authenticated=true, Details=WebAuthenticationDetails [RemoteIpAddress=0:0:0:0:0:0:0:1, SessionId=F8D87A2A561577B39AE416F781269480], Granted Authorities=[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]]] from SPRING_SECURITY_CONTEXT
Did not set SecurityContextHolder since already authenticated OAuth2AuthenticationToken [Principal=Name: [116396123335717576796], Granted Authorities: [[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]], User Attributes: [{at_hash=8c4_6SnlseoVm9WZqlA6WQ, sub=116396123335717576796, email_verified=true, iss=https://accounts.google.com, given_name=Kamil, nonce=7d9jDo6OpQZGveB4WJkTOHVj1eSnS7igpnDkFO_GBZw, picture=https://lh3.googleusercontent.com/a/ACg8ocJ9CV8HJxfxYqHdvHGJLXlpfdEhwmtlLOdrSG3lRS6MrdmIMw=s96-c, aud=[75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com], azp=75783613-3k0cpbta315bfvc91ltcthouapl06ja4.apps.googleusercontent.com, name=Kamil, exp=2024-05-04T10:48:48Z, iat=2024-05-04T09:48:48Z, email=kuchtakamil@gmail.com}], Credentials=[PROTECTED], Authenticated=true, Details=WebAuthenticationDetails [RemoteIpAddress=0:0:0:0:0:0:0:1, SessionId=F8D87A2A561577B39AE416F781269480], Granted Authorities=[OIDC_USER, SCOPE_https://www.googleapis.com/auth/userinfo.email, SCOPE_https://www.googleapis.com/auth/userinfo.profile, SCOPE_openid]]
Secured GET /error?continue
Not injecting HSTS header since it did not match request to [Is Secure]


---

**Assistant:**

It looks like your application is successfully redirecting to the Google OAuth2 login page and authenticating the user successfully, but then there seems to be an issue when redirecting back to your application after authentication. 

The logs indicate that the redirection to `http://localhost:8080/error?continue` is happening, but it seems that this endpoint is not properly handling the authentication callback from Google. The error status code 999 usually indicates a generic error, and in this case, it might be due to a misconfiguration or an issue in handling the callback from the OAuth2 provider.

Here are a few steps you can take to debug and resolve the issue:

1. **Check Redirect URIs**: Ensure that the redirect URI configured in your Google OAuth2 client matches the one you're using in your application (`http://localhost:8080/login/oauth2/code/google`). If they don't match, Google will not redirect back to your application properly.

2. **Check Error Handling**: Review the error handling in your `/error` endpoint. It seems like this endpoint is being hit after the OAuth2 authentication, so make sure it can properly handle the callback and retrieve the authentication details from the request.

3. **Debug Logs**: Add more logging to your `/error` endpoint to see if you can get more information about what's going wrong. You might be able to log the request parameters or any exceptions that are occurring.

4. **Verify OAuth2 Configuration**: Double-check your OAuth2 configuration in your Spring Security configuration files to ensure everything is set up correctly. Make sure the client ID, client secret, and other configuration details are accurate.

5. **Check Dependencies**: Ensure that you have all the necessary dependencies for OAuth2 integration in your `pom.xml` or `build.gradle` file, and they are compatible with your Spring Boot version.

By following these steps and carefully examining the logs and configurations, you should be able to identify and resolve the issue with your OAuth2 authentication callback.

---

**User:**

ok.
I have that
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .anonymous(Customizer.withDefaults())
                .authorizeHttpRequests(auth -> {
                    auth.requestMatchers("/").permitAll();
                    auth.requestMatchers("/favicon.ico").permitAll();
                    auth.anyRequest().authenticated();
                })
                .oauth2Login(withDefaults())
                .formLogin(withDefaults())
                .build();
    }
} 
and some basic rest controllers.
And I want to fetch a authorization token which is created after the login process.

---

**Assistant:**

To fetch the authorization token after the login process in a Spring Security OAuth2 setup, you can access the authentication object and extract the token from it. Since you're using OAuth2 login, the authentication object should be of type `OAuth2AuthenticationToken`.

Here's how you can modify your existing setup to fetch the authorization token:

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
                .anonymous(Customizer.withDefaults())
                .authorizeHttpRequests(auth -> {
                    auth.requestMatchers("/").permitAll();
                    auth.requestMatchers("/favicon.ico").permitAll();
                    auth.anyRequest().authenticated();
                })
                .oauth2Login(withDefaults())
                .formLogin(withDefaults())
                .and()
                .oauth2Login()
                .userInfoEndpoint()
                .userService(oAuth2UserService())
                .and()
                .defaultSuccessUrl("/profile")
                .and()
                .oauth2Client()
                .and()
                .build();
    }

    @Bean
    public OAuth2UserService<OidcUserRequest, OidcUser> oAuth2UserService() {
        return new DefaultOAuth2UserService();
    }

    @GetMapping("/profile")
    public String profile(HttpServletRequest request) {
        OAuth2AuthenticationToken authentication = (OAuth2AuthenticationToken) SecurityContextHolder.getContext().getAuthentication();
        OAuth2AuthorizedClient authorizedClient = authorizedClientService.loadAuthorizedClient(
                authentication.getAuthorizedClientRegistrationId(),
                authentication.getName());

        OAuth2AccessToken accessToken = authorizedClient.getAccessToken();
        String tokenValue = accessToken.getTokenValue();

        // Now you have the access token, you can use it to fetch user information or make API calls.
        // You may want to redirect or render a page with the token value.
        return "profile";
    }
}
```

In this code:

1. We've added an additional `oauth2Login()` configuration to specify the `userInfoEndpoint()` and set the `userService()` to a `DefaultOAuth2UserService`.
2. We've added a `profile()` method which handles the `/profile` endpoint. Inside this method, we extract the authentication object and then use the `authorizedClientService` to load the authorized client, from which we can obtain the access token.
3. You can use the access token to make authorized API calls or fetch user information.

Make sure to import the necessary classes (`OAuth2AuthenticationToken`, `OAuth2AuthorizedClient`, `OAuth2AccessToken`, `DefaultOAuth2UserService`, etc.) and inject any required dependencies such as `OAuth2AuthorizedClientService`.