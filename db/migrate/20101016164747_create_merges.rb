class CreateMerges < ActiveRecord::Migration
  def self.up
    create_table :merges do |t|
      t.text :message

      t.timestamps
    end
  end

  def self.down
    drop_table :merges
  end
end
