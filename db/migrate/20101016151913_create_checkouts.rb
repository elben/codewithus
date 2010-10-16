class CreateCheckouts < ActiveRecord::Migration
  def self.up
    create_table :checkouts do |t|
      t.string :active_branch

      t.timestamps
    end
  end

  def self.down
    drop_table :checkouts
  end
end
