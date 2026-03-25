# Async server name retrieval.

**Data:** 2023-03-24

---

**User:**

import scala.concurrent.{ExecutionContext, Future}

/**
 * Implement logic:
 * - take a web-page URL
 * - load the web-page body, extracts HTTP links from it
 * - for all the found links, try to fetch a server name header if there is one
 * - return all the encountered unique server name values in alphabetical order
 *
 * Each link processing should be done in parallel.
 * Validation of arguments is not needed.
 *
 * Try to test it on https://google.com using AsyncHomeworkApp!
 */
abstract class AsyncHomework {
  protected implicit def ec: ExecutionContext

  //-- these methods are provided to you!
  protected def fetchPageBody(url: String): Future[String]
  protected def fetchServerName(url: String): Future[Option[String]]
  protected def findLinkUrls(html: String): Future[Vector[String]]
  //--

  final def fetchUniqueSortedServerNamesFromPageLinks(url: String): Future[Vector[String]] = {
    //put your code there
    ???
  }
}

---

**Assistant:**



To implement the `fetchUniqueSortedServerNamesFromPageLinks` method, we need to follow these steps:

1. Fetch the web-page body for the given URL using `fetchPageBody` method.
2. Find all the HTTP links in the page using `findLinkUrls` method.
3. For each link, fetch the server name header using `fetchServerName` method.
4. Collect all the unique server names encountered in the step above.
5. Sort the unique server names in alphabetical order.
6. Return the sorted unique server names as the result.

Here is the implementation of `fetchUniqueSortedServerNamesFromPageLinks` method:

```scala
final def fetchUniqueSortedServerNamesFromPageLinks(url: String): Future[Vector[String]] = {
  for {
    pageBody <- fetchPageBody(url)
    links <- findLinkUrls(pageBody)
    serverNames <- Future.sequence(links.map(fetchServerName)).map(_.flatten.distinct.sorted)
  } yield serverNames
}
```

Here, we use `for` comprehension to compose the different asynchronous operations. We first fetch the page body for the given URL using `fetchPageBody` method. Then we find all the HTTP links in the page using `findLinkUrls` method. For each link, we fetch the server name header using `fetchServerName` method by mapping over the links and using `Future.sequence` to execute the fetch operations in parallel. We flatten the result of server names for all the links, remove duplicates using `distinct`, and sort them in alphabetical order using `sorted`. Finally, we return the sorted unique server names as the result.