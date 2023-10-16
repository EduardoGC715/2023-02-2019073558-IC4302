CREATE TABLE IF NOT EXISTS pokemons (
                primaryKey SERIAL PRIMARY KEY,
                pokemonId VARCHAR(255),
                PokemonName VARCHAR(255),
                Type1 VARCHAR(255),
                Type2 VARCHAR(255),
                Category VARCHAR(255),
                Heightf VARCHAR(255),
                Heightm VARCHAR(255),
                Weightlbs VARCHAR(255),
                Weightkg VARCHAR(255),
                CaptureRate VARCHAR(255),
                EggSteps VARCHAR(255),
                ExpGroup VARCHAR(255),
                Total VARCHAR(255),
                HP VARCHAR(255),
                Attack VARCHAR(255),
                Defense VARCHAR(255),
                SpAttack VARCHAR(255),
                SpDefense VARCHAR(255),
                Speed VARCHAR(255)
            );
			
INSERT INTO pokemons (
    pokemonId, PokemonName, Type1, Type2, Category, Heightf, Heightm, Weightlbs, Weightkg, CaptureRate, EggSteps, ExpGroup, Total, HP, Attack, Defense, SpAttack, SpDefense, Speed
)
VALUES (
    '001', 'Bulbasaur', 'Grass', 'Poison', 'Seed Pokémon', '2.04', '0.7', '15.2', '6.9', '45', '5120', 'Medium Slow', '318', '45', '49', '49', '65', '65', '45'
);

DELETE FROM pokemons
WHERE pokemonId = '001';

SELECT * FROM pokemons;
			
