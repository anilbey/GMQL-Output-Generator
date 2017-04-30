"""

General purpose parser for the output of the MAP operations of GMQL

"""

import pandas as pd
import os
import xml.etree.ElementTree


class OutputGenerator:

    def __init__(self,path):
        self.path = path
        self.data = None
        self.meta_data = None
        return

    def get_sample_name(self, path):
        sp = path.split('/')
        file_name = sp[-1]
        return file_name.split('.')[0]

    def _get_files(self, extension, path):
        # retrieves the files sharing the same extension
        files = []
        for file in os.listdir(path):
            if file.endswith(extension):
                files.append(os.path.join(path, file))
        return sorted(files)

    def _get_file(self, extension):
        for file in os.listdir(self.path):
            if file.endswith(extension):
                return os.path.join(self.path, file)


    def parse_schema(self, schema_file):
        # parses the schema and returns its columns
        e = xml.etree.ElementTree.parse(schema_file)
        root = e.getroot()
        cols = []
        for elem in root.findall(".//{http://genomic.elet.polimi.it/entities}field"):  # XPATH
            cols.append(elem.text)
        return cols

    def read_meta_data(self, fname):
        # reads a meta data file into a dictionary
        d = {}
        with open(fname) as f:
            for line in f:
                (key, val) = line.split('\t')
                d[key] = val
        return d

    def read_all_meta_data(self):
        # reads all meta data files
        files = self._get_files("meta", self.path)
        meta_data = []
        for f in files:
            var = self.read_meta_data(f)
            meta_data.append(var)
        self.meta_data = meta_data


    def read_one(self, path, cols, desired_col):
        # reads a sample file
        df = pd.read_table(path, sep="\t|;", lineterminator="\n")
        df = df.drop(df.columns[[-1]],axis=1)  # the last column is null
        df.columns = cols  # column names from schema
        df = df.drop(df.columns[[1, 2, 5, 7]], axis=1)
        df['region'] = df['seqname'].map(str) + ',' + df['start'].map(str) + '-' + df['end'].map(str) + ',' + df[
            'strand'].map(str)
        sample = self.get_sample_name(path)
        df['sample'] = sample
        desired_cols = ['sample', 'region', desired_col]
        df = df[desired_cols]
        df[desired_col] = df[desired_col].apply(lambda x: x.split('"')[-2] if isinstance(x, str) and (x.find('"') != -1) else x) #if it is a string and contains "
        return df

    def select_columns(self, desired_cols):
        self.data = self.data[desired_cols]



    def read_all(self, path, schema_file,desired_col):
        # reads all sample files
        files = self._get_files("gtf", path)
        df = pd.DataFrame()
        cols = self.parse_schema(schema_file)
        for f in files:
            data = self.read_one(f, cols, desired_col)
            if data is not None:
                df = pd.concat([data, df], axis=0)
        self.data = df

    def to_matrix(self,value):
        # creates a matrix dataframe
        self.data[value] = self.data[value].map(int)
        self.data = pd.pivot_table(self.data,
                                values=value, index=['region'], columns=['sample'],
                                fill_value=0)

    def remove_zeros(self):
        # to remove the zero regions
        self.data = self.data.loc[(self.data != 0).any(1)]

