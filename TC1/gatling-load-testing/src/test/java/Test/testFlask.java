package Test;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;

import java.util.concurrent.ThreadLocalRandom;

public class testFlask extends Simulation {
    // Http Protocol
    HttpProtocolBuilder httpProtocol =
            http.baseUrl("http://127.0.0.1:5000")
                    .acceptHeader("application/json")
                    .contentTypeHeader("application/json");

    //FEEDER FOR TEST DATA
    private static FeederBuilder.FileBased<Object> jsonFeeder = jsonFile("data/pokedex.json").random();

    private static ChainBuilder getAllPokemon =
            exec(http("Get all Pokemon")
                    .get("/getPokemon"));

    private static ChainBuilder addPokemon =
            feed(jsonFeeder)
                    .exec(http("Add new Pokemon - #{Name}")
                            .post("/postPokemon")
                            .body(ElFileBody("bodies/pokemonTemplate.json")).asJson()
                            );

    private static ChainBuilder deleteLastPostedPokemon =
            exec(http("Delete Pokemon - #{name}").delete("/deletePokemon/#{id}").check(bodyString().is("Video game deleted")));
    // Scenario
    ScenarioBuilder scn = scenario("Database stress test")
            .feed(jsonFeeder)
            .exec(getAllPokemon)
            .pause(2)
            .exec(addPokemon)
            .pause(2);
    {
        setUp(
                scn.injectOpen(atOnceUsers(10))
        ).protocols(httpProtocol);
    }
}
