package Test;

public class Pokemon {
    private String id;
    private String name;
    private String type1;
    private String type2;

    private String category;
    private String heightf;
    private String heightm;
    private String weightlbs;
    private String weightkg;
    private String captureRate;
    private String eggSteps;
    private String expGroup;
    private String total;
    private String hp;
    private String attack;
    private String defense;
    private String spattack;
    private String spdefense;
    private String speed;

    public void setId(String id) {
        this.id = id;
    }

    public String getType1() {
        return type1;
    }

    public String getWeightkg() {
        return weightkg;
    }

    public void setWeightkg(String weightkg) {
        this.weightkg = weightkg;
    }

    public String getCaptureRate() {
        return captureRate;
    }

    public void setCaptureRate(String captureRate) {
        this.captureRate = captureRate;
    }

    public String getEggSteps() {
        return eggSteps;
    }

    public void setEggSteps(String eggSteps) {
        this.eggSteps = eggSteps;
    }

    public String getExpGroup() {
        return expGroup;
    }

    public void setExpGroup(String expGroup) {
        this.expGroup = expGroup;
    }

    public String getTotal() {
        return total;
    }

    public void setTotal(String total) {
        this.total = total;
    }

    public String getHp() {
        return hp;
    }

    public void setHp(String hp) {
        this.hp = hp;
    }

    public String getAttack() {
        return attack;
    }

    public void setAttack(String attack) {
        this.attack = attack;
    }

    public String getDefense() {
        return defense;
    }

    public void setDefense(String defense) {
        this.defense = defense;
    }

    public String getSpattack() {
        return spattack;
    }

    public void setSpattack(String spattack) {
        this.spattack = spattack;
    }

    public String getSpdefense() {
        return spdefense;
    }

    public void setSpdefense(String spdefense) {
        this.spdefense = spdefense;
    }

    public String getSpeed() {
        return speed;
    }

    public void setSpeed(String speed) {
        this.speed = speed;
    }

    public void setType1(String type1) {
        this.type1 = type1;
    }

    public String getType2() {
        return type2;
    }

    public void setType2(String type2) {
        this.type2 = type2;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getHeightf() {
        return heightf;
    }

    public void setHeightf(String heightf) {
        this.heightf = heightf;
    }

    public String getHeightm() {
        return heightm;
    }

    public void setHeightm(String heightm) {
        this.heightm = heightm;
    }

    public String getWeightlbs() {
        return weightlbs;
    }

    public void setWeightlbs(String weightlbs) {
        this.weightlbs = weightlbs;
    }

    // Default constructor (required for Jackson deserialization)
    public Pokemon() {
    }

    // Getters and setters (or use Lombok for automatic generation)

    public String getId() {
        return id;
    }

    public void setId(int id) {
        this.id = String.valueOf(id);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }




    @Override
    public String toString() {
        return "{\n" +
                "    \"Id\": \""+id+"\",\n" +
                "    \"Name\": \""+name+"\",\n" +
                "    \"Type1\": \""+type1+"\",\n" +
                "    \"Type2\": \""+type2+"\",\n" +
                "    \"Category\": \""+category+"\",\n" +
                "    \"Heightf\": \""+heightf+"\",\n" +
                "    \"Heightm\": \""+heightm+"\",\n" +
                "    \"Weightlbs\": \""+weightlbs+"\",\n" +
                "    \"Weightkg\": \""+weightkg+"\",\n" +
                "    \"CaptureRate\": \""+captureRate+"\",\n" +
                "    \"EggSteps\": \""+eggSteps+"\",\n" +
                "    \"ExpGroup\": \""+expGroup+"\",\n" +
                "    \"Total\": \""+total+"\",\n" +
                "    \"HP\": \""+hp+"\",\n" +
                "    \"Attack\": \""+attack+"\",\n" +
                "    \"Defense\": \""+defense+"\",\n" +
                "    \"SpAttack\": \""+spattack+"\",\n" +
                "    \"SpDefense\": \""+spdefense+"\",\n" +
                "    \"Speed\": \""+speed+"\"\n" +
                "  }";
    }

}
