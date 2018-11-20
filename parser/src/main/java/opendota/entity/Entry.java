package opendota.entity;

public class Entry {
    public Integer time = 0;
    public String type;
    public String unit;
    public Integer value;
    public Integer slot;
    //combat log fields
    public String attackername;
    public String targetname;
    public String sourcename;
    public String targetsourcename;
    public Boolean attackerhero;
    public Boolean targethero;
    public Boolean attackerillusion;
    public Boolean targetillusion;
    public String inflictor;
    //entity fields
    public Integer gold;
    public Integer lh;
    public Integer xp;
    public Integer hero_id;

    public Integer level;
    public Integer kills;
    public Integer deaths;
    public Integer assists;
    public Integer denies;
    public Integer roshans_killed;

    //tower and roshan death info
    public Integer rt1t;
    public Integer rt2t;
    public Integer rt3t;
    public Integer rt1m;
    public Integer rt2m;
    public Integer rt3m;
    public Integer rt1b;
    public Integer rt2b;
    public Integer rt3b;

    public Integer rRosh;

    public Integer dt1t;
    public Integer dt2t;
    public Integer dt3t;
    public Integer dt1m;
    public Integer dt2m;
    public Integer dt3m;
    public Integer dt1b;
    public Integer dt2b;
    public Integer dt3b;

    public Integer dRosh;

//    public Integer towers_killed;
//    public Integer item_id;
//    public transient List<Item> hero_inventory;
//		public Integer obs_placed;
//		public Integer sen_placed;
//		public Integer rune_pickups;

    public Entry() {
    }

    public Entry(Integer time) {
        this.time = time;
    }
}