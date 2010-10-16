class CreateCommits < ActiveRecord::Migration
  def self.up
    create_table :commits do |t|
      t.string :author
      t.text :message
      t.string :hash

      t.timestamps
    end
  end

  def self.down
    drop_table :commits
  end
end
