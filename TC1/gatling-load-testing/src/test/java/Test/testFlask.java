package Test;

import static io.gatling.javaapi.core.CoreDsl.*;
import static io.gatling.javaapi.http.HttpDsl.*;

import com.fasterxml.jackson.databind.type.CollectionType;
import com.fasterxml.jackson.databind.type.TypeFactory;
import io.gatling.javaapi.core.*;
import io.gatling.javaapi.http.*;
import com.fasterxml.jackson.databind.ObjectMapper;


import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Random;


import java.util.concurrent.ThreadLocalRandom;

public class testFlask extends Simulation {
    // Http Protocol
    HttpProtocolBuilder httpProtocol =
            http.baseUrl("http://127.0.0.1:54254")
                    .acceptHeader("application/json")
                    .contentTypeHeader("application/json");

    //FEEDER FOR TEST DATA
    private static FeederBuilder.FileBased<Object> jsonFeeder = jsonFile("data/pokedex.json").random();

    private static ChainBuilder getAllPokemon =
            exec(http("Get all Pokemon")
                    .get("/getAllPokemon"));

    private static ChainBuilder getPokemonId =
            feed(jsonFeeder)
                    .exec(http("Get one Pokemon #{Id}")
                    .get("/getPokemon/#{Id}")
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .formParam("Id", "#{Id}")
                    .formParam("Name", "#{Name}"));

    private static ChainBuilder addPokemon =
            feed(jsonFeeder)

                    .exec(http("Add new Pokemon - #{Name}")
                            .post("/postPokemon")
                            .header("Content-Type", "application/x-www-form-urlencoded")
                            .formParam("Id", "#{Id}")
                            .formParam("Name", "#{Name}")
                            .formParam("Type1", "#{Type1}")
                            .formParam("Type2", "#{Type2}")
                            .formParam("Category", "#{Category}")
                            .formParam("Heightf", "#{Heightf}")
                            .formParam("Heightm", "#{Heightm}")
                            .formParam("Weightlbs", "#{Weightlbs}")
                            .formParam("Weightkg", "#{Weightkg}")
                            .formParam("CaptureRate", "#{CaptureRate}")
                            .formParam("EggSteps", "#{EggSteps}")
                            .formParam("ExpGroup", "#{ExpGroup}")
                            .formParam("Total", "#{Total}")
                            .formParam("HP", "#{HP}")
                            .formParam("Attack", "#{Attack}")
                            .formParam("Defense", "#{Defense}")
                            .formParam("SpAttack", "#{SpAttack}")
                            .formParam("SpDefense", "#{SpDefense}")
                            .formParam("Speed", "#{Speed}")
                            );

    private static ChainBuilder updatePokemon =
            feed(jsonFeeder)

                    .exec(http("Update new Pokemon - #{Name}")
                            .put("/putPokemon/#{Id}")
                            .header("Content-Type", "application/x-www-form-urlencoded")
                            .formParam("Id", "#{Id}")
                            .formParam("Name", "#{Name}")
                            .formParam("Type1", "#{Type1}")
                            .formParam("Type2", "#{Type2}")
                            .formParam("Category", "#{Category}")
                            .formParam("Heightf", "#{Heightf}")
                            .formParam("Heightm", "#{Heightm}")
                            .formParam("Weightlbs", "#{Weightlbs}")
                            .formParam("Weightkg", "#{Weightkg}")
                            .formParam("CaptureRate", "#{CaptureRate}")
                            .formParam("EggSteps", "#{EggSteps}")
                            .formParam("ExpGroup", "#{ExpGroup}")
                            .formParam("Total", "#{Total}")
                            .formParam("HP", "#{HP}")
                            .formParam("Attack", "#{Attack}")
                            .formParam("Defense", "#{Defense}")
                            .formParam("SpAttack", "#{SpAttack}")
                            .formParam("SpDefense", "#{SpDefense}")
                            .formParam("Speed", "#{Speed}")
                    );

    private static ChainBuilder deleteLastPostedPokemon =
            feed(jsonFeeder)
                    .exec(http("Delete Pokemon - #{Name}")
                            .delete("/deletePokemon/#{Id}")
                            .header("Content-Type", "application/x-www-form-urlencoded")
                    );

    // Scenario
    ScenarioBuilder scn = scenario("Database stress test with every request type").forever().on(
            pace(15)
                    .feed(jsonFeeder)
                    .exec(addPokemon)
                    .pause(2)
                    .feed(jsonFeeder)
                    .exec(getPokemonId)
                    .pause(2)
                    .feed(jsonFeeder)
                    .exec(updatePokemon)
                    .pause(2)
                    .exec(getAllPokemon)
                    .pause(2)
                    .feed(jsonFeeder)
                    .exec(deleteLastPostedPokemon)
                    .pause(2)
    );

    {
        setUp(
                scn.injectOpen(rampUsers(20).during(30))
        ).protocols(httpProtocol).maxDuration(900);
    }
}
