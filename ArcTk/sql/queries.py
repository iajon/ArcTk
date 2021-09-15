import sqlite3 as sl
import os.path
import pandas as pd

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
        self.cur.execute("""INSERT INTO bags (bag_prov, bag_cat_num, bag_other, bag_name, bag_date, bag_active, box_id, newln_ct) 
                        VALUES (?, ?, ?, ?, ?, 1,
                        (SELECT box_id FROM boxes WHERE box_active = 1), ?);""",
                        (bag.prov, bag.cat_num, bag.other, bag.name, bag.date, bag.card.newln_ct))
        
        
        # Insert into artifacts table
        for artifact in bag.__dict__['artifact_ls']:
            try:
                self.cur.execute("""INSERT INTO artifacts (artifact_count, artifact_weight, bag_id, artifact_type_id) 
                                VALUES (?, ?,
                                (SELECT bag_id FROM bags WHERE bag_active = 1),
                                (SELECT artifact_type_id FROM artifact_types WHERE artifact_type_name = ?));""", 
                                (artifact.ARTIFACT_COUNT, artifact.ARTIFACT_WEIGHT, artifact.ARTIFACT_TYPE))
            except:
                
                self.cur.execute("""INSERT INTO artifacts (artifact_count, artifact_weight, bag_id, artifact_type_id) 
                                VALUES (?, ?,
                                (SELECT bag_id FROM bags WHERE bag_active = 1),
                                (SELECT artifact_type_id FROM artifact_types WHERE artifact_type_name = ?));""", 
                                (artifact.ARTIFACT_COUNT, artifact.ARTIFACT_WEIGHT, 'Unidentified'))
        
        self.con.commit()
    
    def get_pdf_collate_view(self):
        self.cur.execute("SELECT * FROM pdf_collate_view;")

        # Get all as list
        ls = []
        for i in self.cur.fetchall():
            ls.append(list(i))
        print(ls)
        
        # Append to ids
        for i in ls:
            ids.append(ls[1])
        # Set ids as carded
        for id in ids:
            self.cur.execute("""UPDATE bags SET carded = 1
                                WHERE bag_id = ?;""",(id,))


        # Grab bags
        bag_data = []
        for id in ids:
            self.cur.execute("""SELECT * FROM full_box_view
                              WHERE bags.bag_id = ?;""", (id,))
            for i in self.cur.fetchall():
                bag_data.append(list(i))
        
        print('This' + bag_data)

        return(bag_data)



    
    def get_pdf_view(self):
        self.cur.execute("SELECT * FROM full_box_view;")

        ls = []
        for i in self.cur.fetchall():
            ls.append(list(i))
        
        target = 15
        flag = False
        line_num = 0 # By line
        row_num = 0 # By one
        cell = 0 # By iteration
        newln_ls = []
        id_ls = []


        for bag in ls:
            if flag == False:
                if bag[9] not in id_ls:
                    id_ls.append(bag[9])

                    if cell == 0:
                        row_num += 1
                        line_num += bag[10]

                    elif cell >= 4:
                        cell = -1
                        if line_num >= target:
                            flag = True
                    cell += 1
        print(line_num)
        print(row_num)
        limit = row_num * 5
        print(limit)

        if flag == True:
            return self.get_pdf_rows(limit)
        else:
            return False

    def get_pdf_rows(self, limit):
        self.cur.execute("""SELECT * FROM (SELECT * FROM pdf_view LIMIT 0,?) pdf_view
                            LEFT JOIN 
                            artifacts 
                            ON artifacts.bag_id = pdf_view.bag_id
                            LEFT JOIN 
                            artifact_types 
                            ON artifact_types.artifact_type_id = artifacts.artifact_type_id""", (limit,))
        ls = []
        for i in self.cur.fetchall():
            ls.append(list(i))
            print(ls[-1])
        
        return ls
    
    def update_carded(self, id):
        self.cur.execute("""UPDATE bags
                            SET carded = 1
                            WHERE bag_id = ?;""",
                            (id,))
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
    
    def get_bag(self, id):
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
    
    def get_bag_ids(self):
        self.cur.execute("""SELECT bags.bag_id FROM bags
                            INNER JOIN boxes ON boxes.box_id = bags.box_id
                            WHERE boxes.box_active = 1""")
        
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
        
        return self.cur.fetchall()

    def get_bag_by_id(self, id):
        # Select all bags from active box
        self.cur.execute("""SELECT bags.bag_prov, bags.bag_cat_num, bags.bag_other, bags.bag_name, bags.bag_date
                            FROM bags
                            WHERE bags.bag_id=?""", (id,))
        
        # Return selection
        return list(self.cur.fetchall()[0])

    def get_artifact_by_id(self, id):
        # Select all bags from active box
        self.cur.execute("""SELECT artifact_types.artifact_type_name, artifacts.artifact_count, artifacts.artifact_weight
                            FROM artifacts
                            INNER JOIN artifact_types ON artifact_types.artifact_type_id = artifacts.artifact_type_id
                            INNER JOIN bags ON bags.bag_id = artifacts.bag_id
                            WHERE bags.bag_id = ?""", (id,))
        
        # Return selection
        ls = []
        for i in self.cur.fetchall():
            ls.append(list(i))
        
        return ls

    def delete_bag(self, id):
        self.cur.execute("""DELETE FROM artifacts 
                            WHERE artifacts.bag_id = ?;""", (id,))
        
        self.cur.execute("""DELETE FROM bags 
                            WHERE bags.bag_id = ?;""", (id,))

        self.con.commit()

    def get_count(self):
        self.cur.execute("""SELECT COUNT(*) FROM bags
                            INNER JOIN boxes ON boxes.box_id = bags.box_id
                            WHERE boxes.box_active = 1;""")

        return list(self.cur.fetchall()[0])[0]
        

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

    def sql_to_excel(self):
        df = pd.read_sql_query("SELECT * FROM export_view", self.con)

        return df
        
def main():
    pass

if __name__ == "__main__":
    main()
