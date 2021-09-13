import sqlite3 as sl
import os.path

class Connection:
    def __init__(self, filename):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(BASE_DIR, filename)

        self.con = sl.connect(filepath)
        self.cur = self.con.cursor()

    def insert_box(self, box, active):
        # Set all boxes as inactive IFF this box is to be active
        if active == 1:
            self.cur.execute("UPDATE boxes SET box_active = 0;")
        
        # Insert into sites table if site does not exist
        self.cur.execute("""INSERT INTO sites (site_number, site_name, county_id) 
                        SELECT ?, ?, (SELECT county_id FROM counties WHERE county_abbreviation = ?) 
                        WHERE NOT EXISTS (SELECT * FROM sites WHERE site_number = ?);""", 
                        (box.site_num, box.site_name, box.county, box.site_num))

        # Insert into boxes table
        self.cur.execute("""INSERT INTO boxes (box_oin, box_sn, box_in, box_collectors, box_years, box_pname, box_ptype, box_contract, site_id, box_active) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ? ,
                        (SELECT site_id FROM sites WHERE site_number = ?), ?);""", 
                        (box.oin, box.shelving_num, box.id_num, box.collectors, box.years, box.pname, box.ptype, box.contract, box.site_num, active))

        self.con.commit()

    def insert_bag(self, bag):
        # Set all bags as inactive
        self.cur.execute("UPDATE bags SET bag_active = 0;")

        # Insert into bags table
        self.cur.execute("""INSERT INTO bags (bag_prov, bag_cat_num, bag_other, bag_name, bag_date, bag_active, box_id) 
                        VALUES (?, ?, ?, ?, ?, 1,
                        (SELECT box_id FROM boxes WHERE box_active = 1));""",
                        (bag.prov, bag.cat_num, bag.other, bag.name, bag.date))
        
        # Insert into artifacts table
        for artifact in bag.artifact_ls:
            self.cur.execute("""INSERT INTO artifacts (artifact_count, artifact_weight, bag_id, artifact_type_id) 
                            VALUES (?, ?,
                            (SELECT bag_id FROM bags WHERE bag_active = 1),
                            (SELECT artifact_type_id FROM artifact_types WHERE artifact_type_name = ?));""", 
                            (artifact.ARTIFACT_COUNT, artifact.ARTIFACT_WEIGHT, artifact.ARTIFACT_TYPE))

        self.con.commit()

    def update_box(self, box, target = "active"):
        if target == "active":
            target_str = "WHERE boxes.box_active = 1"

        # Insert into sites iff site does not exist
        self.cur.execute("""INSERT INTO sites (site_number, site_name, county_id) 
                        select ?, ?, (SELECT county_id FROM counties WHERE county_abbreviation = ?)
                        WHERE NOT EXISTS (SELECT * FROM sites WHERE site_number = ?);""", 
                        (box.site_num, box.site_name, box.county, box.site_num))

        # Even if site exists, update site name
        self.cur.execute("""UPDATE sites
                            SET site_name = ?
                            WHERE site_number = ?;""",
                            (box.site_name, box.site_num))

        # Update box
        self.cur.execute(f"""UPDATE boxes
                            SET box_oin = ?,
                                box_sn = ?,
                                box_in = ?,
                                box_collectors = ?,
                                box_years = ?,
                                box_pname = ?,
                                box_ptype = ?,
                                box_contract = ?,
                                site_id = (SELECT site_id FROM sites WHERE site_number = ?)
                            {target_str}""",
                            (box.oin, box.shelving_num, box.id_num, box.collectors, box.years, box.pname, box.ptype, box.contract, box.site_num))
        self.con.commit()

    def set_active_box(self, target):
        # Set all boxes inactive
        self.cur.execute("UPDATE boxes SET box_active = 0;")

        # Set target as active
        self.cur.execute("""UPDATE boxes
                            SET box_active = 1
                            WHERE box_id = ?;""",
                            (target,))

        self.con.commit()

    def get_active_box(self):
        self.cur.execute("SELECT * FROM active_box_view")

        # Return selection
        return self.cur.fetchall()

    def get_box_for_export(self):
        self.cur.execute("SELECT * FROM export_view")

        # Return selection
        return self.cur.fetchall()
        
    def get_box_ids(self):
        self.cur.execute("""SELECT boxes.box_id
                            FROM boxes""")
        
        return self.cur.fetchall()

    def get_artifacts(self):
        # Select all artifacts
        self.cur.execute("""SELECT artifact_types.artifact_type_name, artifacts.artifact_count, artifacts.artifact_weight
                        FROM artifacts
                        INNER JOIN artifact_types ON artifacts.artifact_type_id=artifact_types.artifact_type_id;""")

    def get_bag_by_active(self):
        # Select active bag
        self.cur.execute("""SELECT bags.bag_id, sites.site_number, bags.bag_prov, bags.bag_cat_num, bags.bag_other, bags.bag_name, bags.bag_date, artifact_types.artifact_type_name, artifacts.artifact_count, artifacts.artifact_weight
                            FROM bags
                            INNER JOIN boxes ON boxes.box_id = bags.box_id
                            INNER JOIN sites ON sites.site_id = boxes.site_id
                            INNER JOIN artifacts ON artifacts.bag_id = bags.bag_id
                            INNER JOIN artifact_types ON artifact_types.artifact_type_id = artifacts.artifact_type_id
                            WHERE bags.bag_active = 1;""")
        
        # Return selection

        return self.cur.fetchall()

    def get_bag_by_box(self):
        # Select all bags from active box
        self.cur.execute("""SELECT bags.bag_id, sites.site_number, bags.bag_prov, bags.bag_cat_num, bags.bag_other, bags.bag_name, bags.bag_date, artifact_types.artifact_type_name, artifacts.artifact_count, artifacts.artifact_weight
                            FROM bags
                            INNER JOIN boxes ON boxes.box_id = bags.box_id
                            INNER JOIN sites ON sites.site_id = boxes.site_id
                            INNER JOIN artifacts ON artifacts.bag_id = bags.bag_id
                            INNER JOIN artifact_types ON artifact_types.artifact_type_id = artifacts.artifact_type_id
                            WHERE boxes.box_active = 1""")
        
        # Return selection
        return self.cur.fetchall()

    def get_box(self, target = "active"):
        # Select active
        if target == "active":
            self.cur.execute("SELECT * FROM active_box_view")
        
        # Select by id
        else:
            self.cur.execute(f"SELECT * FROM box_view WHERE boxes.box_id = {target}")

        # Return selection
        return self.cur.fetchall()
        
    
        
    def get_box_by_unprocessed(self):
        self.cur.execute("SELECT * FROM unprocessed_box_view")
        
        # Return selection
        return self.cur.fetchall()
        
def main():
    pass

if __name__ == "__main__":
    main()
