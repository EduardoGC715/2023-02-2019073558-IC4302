package Test;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;

import java.util.concurrent.ThreadLocalRandom;

public class testFlask extends Simulation {
    // Http Protocol
    HttpProtocolBuilder httpProtocol =
            http.baseUrl("http://127.0.0.1:5000");

    // Scenario
    ScenarioBuilder scn = scenario("Insert")
            .exec(http("Insert")
                    .get("/insert"));

    {
        setUp(
                scn.injectOpen(atOnceUsers(10))
        ).protocols(httpProtocol);
    }
}
